import time
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP, Context

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.exc import SQLAlchemyError

mcp = FastMCP("db-runner-mcp")

# -----------------------
# Models
# -----------------------

class DBTestInput(BaseModel):
    engine_url: str = Field(..., description="SQLAlchemy-style URL, e.g., postgresql+psycopg2://user:pass@host:5432/dbname")

class DBQueryInput(BaseModel):
    engine_url: str = Field(..., description="SQLAlchemy-style URL")
    sql: str = Field(..., description="SQL to execute; single statement")
    params: Dict[str, Any] = Field(default_factory=dict, description="Named parameters for SQLAlchemy text()")
    allow_mutation: bool = Field(default=False, description="Set true to allow INSERT/UPDATE/DELETE/DDL")
    max_rows: int = Field(default=1000, description="Max rows to return")
    timeout_seconds: int = Field(default=60, description="Statement timeout at driver/DB (best-effort)")
    autocommit: bool = Field(default=False, description="Commit transaction automatically (mutations only)")

# -----------------------
# Helpers
# -----------------------

def _is_read_only_sql(sql: str) -> bool:
    # Basic safeguard: permit SELECT, WITH (CTE), EXPLAIN, SHOW, DESCRIBE
    s = sql.strip().lower()
    allowed_prefixes = ("select", "with", "explain", "show", "describe")
    return s.startswith(allowed_prefixes)

def _preprocess_sqlplus_script(sql_content: str) -> List[str]:
    """
    Preprocess SQL*Plus scripts to extract executable SQL statements.
    Removes SQL*Plus specific commands and splits into individual statements.
    
    Returns a list of executable SQL statements.
    """
    lines = sql_content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line_stripped = line.strip()
        line_lower = line_stripped.lower()
        
        # Skip SQL*Plus specific commands
        if (line_lower.startswith('set ') or 
            line_lower.startswith('rem ') or
            line_lower.startswith('@') or
            line_lower.startswith('show ') or
            line_lower.startswith('prompt ') or
            line_lower.startswith('spool ') or
            line_lower.startswith('whenever ') or
            line_lower.startswith('define ') or
            line_lower.startswith('exit') or
            not line_stripped):
            continue
        
        # Add the line
        cleaned_lines.append(line)
    
    # Join lines back together
    cleaned_sql = '\n'.join(cleaned_lines)
    
    # Split by forward slash (SQL*Plus statement separator)
    # The forward slash on its own line is the separator
    statements = []
    current_statement = []
    
    for line in cleaned_sql.split('\n'):
        line_stripped = line.strip()
        if line_stripped == '/':
            # End of statement
            if current_statement:
                stmt = '\n'.join(current_statement).strip()
                if stmt:
                    statements.append(stmt)
                current_statement = []
        else:
            current_statement.append(line)
    
    # Don't forget the last statement if there's no trailing /
    if current_statement:
        stmt = '\n'.join(current_statement).strip()
        if stmt:
            statements.append(stmt)
    
    return statements

def _create_engine_safe(url: str, timeout_seconds: int) -> Engine:
    # pool_pre_ping helps with stale connections
    # echo=False for quiet logs; you can enable echo in dev
    engine = create_engine(
        url,
        pool_pre_ping=True,
        pool_recycle=1800,
        future=True
    )
    # Some drivers support per-connection or per-execution timeouts via execution_options or URL params.
    # You can extend this to inject timeouts for specific dialects (e.g., SET LOCAL statement_timeout for Postgres).
    return engine

# -----------------------
# Oracle Defaults
# -----------------------

# Default Oracle connection URL requested by user
ORACLE_URL = "oracle+oracledb://urel_241:urel_241@localhost:1521/?service_name=wind12c"

# Default BAC SQL scripts base path
BAC_SQL_BASE_PATH = "\\\\wsl.localhost\\WindchillVM\\opt\\ptc\\urel_241\\Windchill\\db\\sql\\wnc\\BAC\\wt\\"


# Plain function: connect to DB and return a Connection
def connect_db(engine_url: str = ORACLE_URL, timeout_seconds: int = 60) -> Connection:
    engine = _create_engine_safe(engine_url, timeout_seconds)
    return engine.connect()

# -----------------------
# Tools
# -----------------------

@mcp.tool(name="test_connection", description="Try connecting to the database and returns basic metadata")
def db_test_connection(ctx: Context, engine_url: str) -> Dict[str, Any]:
    try:
        engine = _create_engine_safe(engine_url, timeout_seconds=30)
        with engine.connect() as conn:
            # Run a trivial query per dialect (works for most)
            start = time.perf_counter()
            try:
                result = conn.execute(text("SELECT 1"))
            except SQLAlchemyError:
                # Fallback for dialects where SELECT 1 might not work; try something else as needed.
                result = None
            elapsed_ms = int((time.perf_counter() - start) * 1000)
        return {
            "ok": True,
            "engine_url": engine_url,
            "elapsed_ms": elapsed_ms,
            "dialect": engine.dialect.name
        }
    except Exception as e:
        return {"ok": False, "error": str(e), "engine_url": engine_url}

@mcp.tool(name="query", description="Run a SQL query with parameters using SQLAlchemy (read-only by default)")
def db_query(ctx: Context,
             engine_url: str,
             sql: str,
             params: Optional[Dict[str, Any]] = None,
             allow_mutation: bool = False,
             max_rows: int = 1000,
             timeout_seconds: int = 60,
             autocommit: bool = False) -> Dict[str, Any]:
    params = params or {}

    # Guardrail: block mutations unless explicitly allowed
    if not allow_mutation and not _is_read_only_sql(sql):
        return {"ok": False, "error": "Mutation/DDL blocked. Set allow_mutation=true to run non-read-only SQL."}

    try:
        engine = _create_engine_safe(engine_url, timeout_seconds=timeout_seconds)
        start = time.perf_counter()

        # Transaction handling
        with engine.connect() as conn:
            if allow_mutation and autocommit:
                # autocommit style: begin/commit around single statement
                trans = conn.begin()
                try:
                    result = conn.execute(text(sql), params)
                    trans.commit()
                except Exception:
                    trans.rollback()
                    raise
            else:
                result = conn.execute(text(sql), params)

            # Debug: if environment variable set, return raw rows from underlying cursor
            if os.environ.get("DEBUG_DB_RAW"):
                raw_rows = []
                try:
                    # Some drivers expose .cursor or ._cursor; attempt both safely
                    cursor = getattr(result, 'cursor', None) or getattr(result, '_cursor', None)
                    if cursor is not None:
                        # Attempt fetchall and convert to list
                        try:
                            allrows = cursor.fetchall()
                        except Exception:
                            # fall back to iterating result
                            allrows = list(result)
                        for r in allrows:
                            try:
                                raw_rows.append(tuple(r))
                            except Exception:
                                raw_rows.append(r)
                except Exception as e:
                    raw_rows = [f"debug-extract-error: {e}"]
                return {
                    "ok": True,
                    "dialect": engine.dialect.name,
                    "elapsed_ms": int((time.perf_counter() - start) * 1000),
                    "columns": list(result.keys()) if getattr(result, 'returns_rows', False) else [],
                    "raw_rows": raw_rows,
                }

            # Try to fetch rows if it returns a result set
            rows: List[List[Any]] = []
            columns: List[str] = []
            rowcount: Optional[int] = None
            try:
                if result.returns_rows:
                    columns = list(result.keys())
                    for i, row in enumerate(result):
                        if i >= max_rows:
                            break
                        rows.append([row[c] for c in columns])
                rowcount = result.rowcount
            except Exception:
                # Not all drivers return keys/rowcount similarly
                pass

        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return {
            "ok": True,
            "dialect": engine.dialect.name,
            "elapsed_ms": elapsed_ms,
            "columns": columns,
            "rows": rows,
            "rowcount": rowcount,
            "truncated": len(rows) >= max_rows
        }

    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool(name="execute_bac_sql_scripts", 
          description="Find and execute BAC SQL scripts (create/make table and index) from object directory")
def execute_bac_sql_scripts(ctx: Context,
                            bac_directory: Optional[str] = None,
                            sql_base_path: Optional[str] = None,
                            object_directory: Optional[str] = None,
                            engine_url: str = ORACLE_URL,
                            timeout_seconds: int = 120,
                            include_drops: bool = False,
                            execute_order: str = "create") -> Dict[str, Any]:
    r"""
    Locates SQL files in BAC directory, categorizes them by type, and executes them in proper order.
    
    Args:
        bac_directory: Direct path to BAC directory (e.g., \\wsl.localhost\WindchillVM\...\wt\change2\bac)
                      If provided, sql_base_path and object_directory are ignored
        sql_base_path: Base path to SQL directory (defaults to BAC_SQL_BASE_PATH constant)
                      Used with object_directory if bac_directory not provided
        object_directory: Object directory name (e.g., "change2" for wt.change2)
                         Used with sql_base_path if bac_directory not provided
        engine_url: Database connection URL (defaults to Oracle)
        timeout_seconds: Timeout for each query execution
        include_drops: Whether to include drop scripts (default: False)
        execute_order: "create" (default) executes creates/makes first, "drop" executes drops first
    
    Returns:
        Dictionary with execution results for each SQL file
    """
    try:
        # Determine BAC directory path
        if bac_directory:
            # Direct path provided
            bac_path = Path(bac_directory)
        elif sql_base_path and object_directory:
            # Construct from base path and object directory
            bac_path = Path(sql_base_path) / object_directory / "bac"
        else:
            # Use default BAC_SQL_BASE_PATH constant
            if object_directory:
                bac_path = Path(BAC_SQL_BASE_PATH) / object_directory / "bac"
            else:
                return {"ok": False, "error": "Must provide either bac_directory, or object_directory, or both sql_base_path and object_directory"}
        
        if not bac_path.exists():
            return {"ok": False, "error": f"Directory not found: {bac_path}"}
        
        # Find SQL files
        sql_files = list(bac_path.glob("*.sql"))
        
        if not sql_files:
            return {"ok": False, "error": f"No SQL files found in {bac_path}"}
        
        # Categorize SQL files by type
        create_tables = []
        create_indexes = []
        drop_tables = []
        drop_indexes = []
        pkg_tables = []
        pkg_indexes = []
        other_files = []
        
        for f in sql_files:
            name_lower = f.name.lower()
            
            # Package operations (Make_pkg_bac, Drop_pkg_bac)
            if "pkg_bac" in name_lower:
                if "table" in name_lower:
                    pkg_tables.append(f)
                elif "index" in name_lower:
                    pkg_indexes.append(f)
                else:
                    other_files.append(f)
            # Drop operations
            elif name_lower.startswith("drop_"):
                if "table" in name_lower:
                    drop_tables.append(f)
                elif "index" in name_lower:
                    drop_indexes.append(f)
                else:
                    other_files.append(f)
            # Create/Make operations
            elif name_lower.startswith("create_") or name_lower.startswith("make_"):
                if "table" in name_lower:
                    create_tables.append(f)
                elif "index" in name_lower:
                    create_indexes.append(f)
                else:
                    other_files.append(f)
            else:
                other_files.append(f)
        
        # Sort each category alphabetically for consistent execution
        create_tables.sort(key=lambda x: x.name)
        create_indexes.sort(key=lambda x: x.name)
        drop_tables.sort(key=lambda x: x.name)
        drop_indexes.sort(key=lambda x: x.name)
        pkg_tables.sort(key=lambda x: x.name)
        pkg_indexes.sort(key=lambda x: x.name)
        
        # Determine execution order based on operation type
        if execute_order == "drop":
            # For drops: indexes first, then tables (reverse of create)
            execution_order = []
            if include_drops:
                execution_order.extend(drop_indexes)
                execution_order.extend(drop_tables)
            execution_order.extend(other_files)
        else:  # create order (default)
            # For creates: tables first, then indexes
            execution_order = []
            execution_order.extend(pkg_tables)      # Package tables first
            execution_order.extend(create_tables)   # Then create tables
            execution_order.extend(pkg_indexes)     # Then package indexes
            execution_order.extend(create_indexes)  # Then create indexes
            if include_drops:
                execution_order.extend(drop_indexes)  # Drops: indexes before tables
                execution_order.extend(drop_tables)
            execution_order.extend(other_files)
        
        results = {
            "ok": True,
            "directory": str(bac_path),
            "files_found": len(sql_files),
            "categorization": {
                "create_tables": len(create_tables),
                "create_indexes": len(create_indexes),
                "drop_tables": len(drop_tables),
                "drop_indexes": len(drop_indexes),
                "pkg_tables": len(pkg_tables),
                "pkg_indexes": len(pkg_indexes),
                "other": len(other_files)
            },
            "execution_results": []
        }
        
        # Connect to database
        engine = _create_engine_safe(engine_url, timeout_seconds=timeout_seconds)
        
        with engine.connect() as conn:
            for sql_file in execution_order:
                file_result = {
                    "file": sql_file.name,
                    "path": str(sql_file),
                    "status": "pending"
                }
                
                try:
                    # Read SQL file
                    sql_content = sql_file.read_text(encoding='utf-8')
                    
                    if not sql_content.strip():
                        file_result["status"] = "skipped"
                        file_result["message"] = "Empty file"
                        results["execution_results"].append(file_result)
                        continue
                    
                    # Preprocess SQL*Plus script into individual statements
                    statements = _preprocess_sqlplus_script(sql_content)
                    
                    if not statements:
                        file_result["status"] = "skipped"
                        file_result["message"] = "No executable SQL statements found"
                        results["execution_results"].append(file_result)
                        continue
                    
                    # Execute each statement
                    file_result["statements_count"] = len(statements)
                    file_result["statements_results"] = []
                    
                    start = time.perf_counter()
                    trans = conn.begin()
                    
                    try:
                        for idx, stmt in enumerate(statements, 1):
                            stmt_result = {"index": idx, "status": "pending"}
                            try:
                                result = conn.execute(text(stmt))
                                stmt_result["status"] = "success"
                                stmt_result["rowcount"] = result.rowcount if hasattr(result, 'rowcount') else None
                            except Exception as stmt_error:
                                stmt_result["status"] = "failed"
                                stmt_result["error"] = str(stmt_error)
                                stmt_result["sql_preview"] = stmt[:200] + "..." if len(stmt) > 200 else stmt
                                file_result["statements_results"].append(stmt_result)
                                raise  # Re-raise to rollback transaction
                            
                            file_result["statements_results"].append(stmt_result)
                        
                        trans.commit()
                        elapsed_ms = int((time.perf_counter() - start) * 1000)
                        
                        file_result["status"] = "success"
                        file_result["elapsed_ms"] = elapsed_ms
                        
                    except Exception as exec_error:
                        trans.rollback()
                        file_result["status"] = "failed"
                        file_result["error"] = str(exec_error)
                        # Continue with other files even if one fails
                        
                except Exception as read_error:
                    file_result["status"] = "failed"
                    file_result["error"] = f"Failed to read file: {str(read_error)}"
                
                results["execution_results"].append(file_result)
        
        # Check if any execution failed
        failed_count = sum(1 for r in results["execution_results"] if r["status"] == "failed")
        if failed_count > 0:
            results["ok"] = False
            results["failed_count"] = failed_count
        
        return results
        
    except Exception as e:
        return {"ok": False, "error": str(e)}


# -----------------------
# Run (stdio)
# -----------------------

if __name__ == "__main__":
    # FastMCP runs a stdio MCP server by default, ideal for Claude Desktop and other MCP clients.
    mcp.run()
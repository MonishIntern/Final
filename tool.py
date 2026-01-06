import json
import os
import re
import uuid
from io import BytesIO
from pathlib import Path
import shutil
from typing import Any, Dict, List, Optional, Tuple

from lxml import etree
from pydantic import BaseModel, Field, ValidationError

from mcp.server.fastmcp import FastMCP, Context

# Root-relative directories
ROOT = Path.cwd()
GH_DIR = ROOT / ".github"
MD_DIR = ROOT / "md"
TEST_DIR = ROOT / "test"

mcp = FastMCP("bac-automation-mcp")

# -----------------------
# Models and helpers
# -----------------------

class Paths(BaseModel):
    wt_path: str
    test_path: str
    object_json_path: str
    bac_src_path: str
    ixl_handler_path: str
    obj_registry_path: str
    service_xconf_path: str
    md_templates_path: str
    test_templates_path: str
    preview: str

def _read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")

def _load_json(p: Path) -> Any:
    return json.loads(_read_text(p))

def _parse_path_config(md: str) -> Paths:
    # Find fenced blocks and pick the one containing key markers
    blocks = re.findall(r"```[\s\S]*?```", md)
    target = None
    for blk in blocks:
        if "wt_path" in blk and "object_json_path" in blk:
            target = blk
            break
    if not target:
        raise ValueError("PATH CONFIGURATION block not found in copilot-instructions.md")

    pairs: Dict[str, str] = {}
    for line in target.splitlines():
        line = line.strip()
        m = re.match(r"^([a-zA-Z_]+)\s*=\s*`?(.+?)`?$", line)
        if m:
            pairs[m.group(1)] = m.group(2)

    required = [
        "wt_path","test_path","object_json_path","bac_src_path","ixl_handler_path",
        "obj_registry_path","service_xconf_path","md_templates_path","test_templates_path","preview"
    ]
    missing = [k for k in required if k not in pairs]
    if missing:
        raise ValueError(f"Missing required path(s): {missing}")

    return Paths(**pairs)

def _allowed_prefixes_from_config(paths: Paths) -> List[str]:
    # Writes are only allowed under these roots
    return [
        paths.wt_path,
        paths.test_path,
        paths.obj_registry_path,
        paths.service_xconf_path,
        paths.bac_src_path,
        paths.ixl_handler_path,
        paths.preview,  # allow BatchPreview output path
        # add schema dirs if you later write XSDs
    ]

def _is_allowed_write(target: str, allowed: List[str]) -> bool:
    # Compare as raw strings, UNC-safe
    for prefix in allowed:
        if target.startswith(prefix):
            return True
    return False

def _atomic_write(path: str, data: bytes) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + f".tmp.{uuid.uuid4().hex}")
    tmp.write_bytes(data)
    os.replace(tmp, p)

def _scan_java_packages(java_dir: str) -> List[Tuple[str, str]]:
    """
    Return list of (fqcn, className) for .java files in java_dir.
    We read the 'package ...;' line and combine with class name.
    """
    out: List[Tuple[str, str]] = []
    base = Path(java_dir)
    if not base.exists():
        return out
    for p in base.glob("*.java"):
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        pkg = None
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("package ") and line.endswith(";"):
                pkg = line[len("package "): -1].strip()
                break
        cls = p.stem
        fqcn = f"{pkg}.{cls}" if pkg else cls
        out.append((fqcn, cls))
    return out

# -----------------------
# Tool inputs
# -----------------------

class RegisterAdminInput(BaseModel):
    template: str = Field(..., description="Object template name (case-sensitive), e.g., WTChangeOrder2")
    registry_file: str = Field(..., description="Full path to the XML registry file to edit (no assumptions)")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Extra attributes to include")
    dry_run: bool = Field(default=True, description="If true, only validate and return intended changes")

class RegisterServicesInput(BaseModel):
    delegate_folder: str = Field(..., description="Folder with generated delegate .java files")
    service_xconf: Optional[str] = Field(None, description="Full path to BAC-service.properties.xconf; if omitted, uses configured service_xconf_path if it points to a file")
    selector: str = Field(..., description="Selector value (typically the template or CollectionCategory key)")
    dry_run: bool = Field(default=True)

class RegisterCategoryInput(BaseModel):
    source_file: str = Field(..., description="Path to CollectionCategory.java (or class with constants)")
    template_name: str = Field(..., description="Exact CASE-SENSITIVE template name to add")
    dry_run: bool = Field(default=True)

class EnsureDirsInput(BaseModel):
    directory_name: str = Field(..., description="Domain directory like wt.change2 or wt.queue")

class WriteFileInput(BaseModel):
    path: str
    content: str
    dry_run: bool = True

class UpdateBACGenericDeleteInput(BaseModel):
    template_name: str = Field(..., description="Template name to add to BACGenericDeleteRecordObjInfos.xsd")
    attributes: List[str] = Field(default_factory=list, description="Optional list of attribute names for the complexType sequence")
    generic_xsd_path: Optional[str] = Field(None, description="Full path to BACGenericDeleteRecordObjInfos.xsd; if omitted, uses configured path")
    dry_run: bool = Field(default=True)

class UpdateBACSpecInput(BaseModel):
    template_name: str = Field(..., description="Template name to add to BACSpec.xsd")
    attributes: List[str] = Field(default_factory=list, description="Optional list of attribute names for the complexType")
    bacspec_xsd_path: Optional[str] = Field(None, description="Full path to BACSpec.xsd; if omitted, uses configured path")
    dry_run: bool = Field(default=True)

class UpdateDeltaControllerInput(BaseModel):
    template_name: str = Field(..., description="Template name (class name) to add to DeltaController")
    controller_path: Optional[str] = Field(None, description="Full path to DeltaController.java; if omitted, searches in configured controllers path")
    dry_run: bool = Field(default=True)

# -----------------------
# Tools
# -----------------------

@mcp.tool(name="read_config", description="Parse PATH CONFIGURATION from .github/copilot-instructions.md")
def read_config(ctx: Context) -> Dict[str, Any]:
    md = _read_text(GH_DIR / "copilot-instructions.md")
    paths = _parse_path_config(md)
    return {"ok": True, "paths": paths.model_dump()}

@mcp.tool(name="read_objects", description="Read .github/object.json and flatten objects including root-level entries")
def read_objects(ctx: Context) -> Dict[str, Any]:
    obj = _load_json(GH_DIR / "object.json")
    flat: Dict[str, Any] = {}
    if isinstance(obj.get("objects"), dict):
        for k, v in obj["objects"].items():
            flat[k] = v
    for k, v in obj.items():
        if k != "objects" and isinstance(v, dict) and "template" in v:
            flat[k] = v
    return {"ok": True, "objects": flat}

# Step 1: Validate and return selected object details
@mcp.tool(name="get_selected_object", description="Validate selected object key and return its properties")
def get_selected_object(ctx: Context, object_key: str) -> Dict[str, Any]:
    obj = _load_json(GH_DIR / "object.json")
    flat: Dict[str, Any] = {}
    if isinstance(obj.get("objects"), dict):
        flat.update(obj["objects"])
    for k, v in obj.items():
        if k != "objects" and isinstance(v, dict) and "template" in v:
            flat[k] = v
    if object_key not in flat:
        return {"ok": False, "error": f"Object '{object_key}' not found. Available: {list(flat.keys())}"}
    selected = flat[object_key]
    required = ["template"]
    missing = [k for k in required if k not in selected]
    if missing:
        return {"ok": False, "error": f"Selected object missing required property(ies): {missing}"}
    directory_name = selected.get("directory") or object_key
    return {
        "ok": True,
        "selected_object": {
            "name": object_key,
            "template": selected["template"],
            "directory": directory_name,
            "key_attributes": selected.get("key_attributes", []),
            "dependencies": selected.get("dependencies", []),
        }
    }

@mcp.tool(name="ensure_directories", description="Create {wt_path}/{dir}/bac and {test_path}/{dir}/bac from config")
def ensure_directories(ctx: Context, directory_name: str) -> Dict[str, Any]:
    md = _read_text(GH_DIR / "copilot-instructions.md")
    paths = _parse_path_config(md)
    wt_dir = Path(paths.wt_path) / directory_name / "bac"
    test_dir = Path(paths.test_path) / directory_name / "bac"
    wt_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)
    return {"ok": True, "created": [str(wt_dir), str(test_dir)]}

@mcp.tool(name="register_admin_object", description="Append an admin object entry to the given XML registry file and validate")
def register_admin_object(ctx: Context, template: str, registry_file: str, properties: Optional[Dict[str, Any]] = None, dry_run: bool = True) -> Dict[str, Any]:
    props = properties or {}
    
    # Always set deleteRecord to the standard value
    props["deleteRecord"] = "com.ptc.windchill.bac.BACGenericDeleteRecord"
    
    rf = Path(registry_file)
    if not rf.exists():
        return {"ok": False, "error": f"Registry file not found: {registry_file}"}

    # Read config for allowlist
    md = _read_text(GH_DIR / "copilot-instructions.md")
    cfg = _parse_path_config(md)
    allowed = _allowed_prefixes_from_config(cfg)
    if not _is_allowed_write(str(rf), allowed):
        return {"ok": False, "error": f"Write blocked: {registry_file} not under allowed prefixes."}

    xml_bytes = rf.read_bytes()
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.fromstring(xml_bytes, parser=parser)
    except Exception as e:
        return {"ok": False, "error": f"Invalid XML in registry file: {e}"}

    # Get namespace from root element
    ns_uri = root.nsmap.get(None)  # Get default namespace
    ns = {"bac": ns_uri} if ns_uri else {}
    
    # Detect registry style: adminObject or <object>
    admin_nodes = root.findall(".//bac:adminObject" if ns_uri else ".//adminObject", namespaces=ns if ns_uri else None)
    use_admin_style = bool(admin_nodes)
    if use_admin_style:
        # Require explicit properties (no assumptions) - deleteRecord is now auto-set
        required = ["collectionCategory", "persistableClass"]
        missing = [k for k in required if k not in props]
        if missing:
            return {"ok": False, "error": f"adminObject registry format detected; missing properties: {missing}"}
        
        # Check for duplicate entry (based on collectionCategory or persistableClass)
        cc_value = str(props["collectionCategory"])
        pc_value = str(props["persistableClass"])
        for existing in admin_nodes:
            existing_cc = existing.find(".//bac:collectionCategory" if ns_uri else ".//collectionCategory", namespaces=ns if ns_uri else None)
            existing_pc = existing.find(".//bac:persistableClass" if ns_uri else ".//persistableClass", namespaces=ns if ns_uri else None)
            if (existing_cc is not None and existing_cc.text == cc_value) or \
               (existing_pc is not None and existing_pc.text == pc_value):
                return {"ok": True, "message": f"Admin object with collectionCategory={cc_value} or persistableClass={pc_value} already exists."}
        
        # Create new adminObject with proper namespace
        if ns_uri:
            admin_el = etree.Element(f"{{{ns_uri}}}adminObject")
            cc = etree.SubElement(admin_el, f"{{{ns_uri}}}collectionCategory")
            cc.text = cc_value
            pc = etree.SubElement(admin_el, f"{{{ns_uri}}}persistableClass")
            pc.text = pc_value
            dr = etree.SubElement(admin_el, f"{{{ns_uri}}}deleteRecord")
            dr.text = str(props["deleteRecord"])
            
            # Add optional dependent elements (support both "dependent" and "dependents" keys)
            dependents_list = []
            if "dependent" in props:
                dependents_list = props["dependent"] if isinstance(props["dependent"], list) else [props["dependent"]]
            elif "dependents" in props:
                dependents_list = props["dependents"] if isinstance(props["dependents"], list) else [props["dependents"]]
            
            for dep in dependents_list:
                dep_el = etree.SubElement(admin_el, f"{{{ns_uri}}}dependent")
                dep_el.text = str(dep)
        else:
            admin_el = etree.Element("adminObject")
            cc = etree.SubElement(admin_el, "collectionCategory")
            cc.text = cc_value
            pc = etree.SubElement(admin_el, "persistableClass")
            pc.text = pc_value
            dr = etree.SubElement(admin_el, "deleteRecord")
            dr.text = str(props["deleteRecord"])
            
            # Add optional dependent elements (support both "dependent" and "dependents" keys)
            dependents_list = []
            if "dependent" in props:
                dependents_list = props["dependent"] if isinstance(props["dependent"], list) else [props["dependent"]]
            elif "dependents" in props:
                dependents_list = props["dependents"] if isinstance(props["dependents"], list) else [props["dependents"]]
            
            for dep in dependents_list:
                dep_el = etree.SubElement(admin_el, "dependent")
                dep_el.text = str(dep)
        
        root.append(admin_el)

    out_bytes = etree.tostring(root, encoding="utf-8", pretty_print=True, xml_declaration=True)
    try:
        etree.fromstring(out_bytes)  # validate well-formedness
    except Exception as e:
        return {"ok": False, "error": f"Generated XML invalid: {e}"}

    if dry_run:
        return {"ok": True, "dry_run": True, "bytes": len(out_bytes)}

    _atomic_write(registry_file, out_bytes)
    return {"ok": True, "dry_run": False, "written": registry_file}

@mcp.tool(name="register_services", description="Ensure all delegates in delegate_folder are registered in BAC-service.properties.xconf (adds missing <Option> only)")
def register_services(ctx: Context, delegate_folder: str, selector: str, service_xconf: Optional[str] = None, dry_run: bool = True) -> Dict[str, Any]:
    md = _read_text(GH_DIR / "copilot-instructions.md")
    cfg = _parse_path_config(md)
    xconf_path = service_xconf or cfg.service_xconf_path

    xconf_file = Path(xconf_path)
    if not xconf_file.exists():
        return {"ok": False, "error": f"xconf not found: {xconf_path}"}

    allowed = _allowed_prefixes_from_config(cfg)
    if not _is_allowed_write(str(xconf_file), allowed):
        return {"ok": False, "error": f"Write blocked: {xconf_path} not under allowed prefixes."}

    classes = _scan_java_packages(delegate_folder)
    if not classes:
        return {"ok": False, "error": f"No .java classes found in {delegate_folder}"}

    xml = xconf_file.read_bytes()
    try:
        parser = etree.XMLParser(remove_blank_text=False, strip_cdata=False)
        doc = etree.parse(BytesIO(xml), parser=parser)
        root = doc.getroot()
    except Exception as e:
        return {"ok": False, "error": f"Invalid xconf XML: {e}"}

    # Map suffix -> service name
    svc_map = {
        "CollectionDelegate": "com.ptc.windchill.bac.delegates.BACCollectionDelegate",
        "DeleteProcessor": "com.ptc.windchill.bac.delegate.BACDeleteProcessor",
        "IdentityDelegate": "wt.ixb.bac.BACIdentityDelegate",
        "ReportDelegate": "com.ptc.windchill.bac.delegates.BACReportDelegate",
        "DeleteTrackingDelegate": "com.ptc.windchill.bac.delegates.BACDeleteTrackingDelegate",
        "DeleteRecordAttributes": "com.ptc.windchill.bac.BACDeleteRecordAttributes",
        "SpecProcessor": "com.ptc.windchill.bac.delegates.BACSpecProcessor"        
    }

    # Build service name -> element map
    svc_by_name = {}
    for s in root.findall(".//Service"):
        name = s.get("name", "")
        if name:
            svc_by_name[name] = s

    added: List[Tuple[str, str]] = []
    for fqcn, cls in classes:
        matched_services: List[str] = []
        for suffix, svc_name in svc_map.items():
            if cls.endswith(suffix) and svc_name in svc_by_name:
                matched_services.append(svc_name)

        for svc_name in matched_services:
            svc_el = svc_by_name[svc_name]
            exists = False
            for opt in svc_el.findall("./Option"):
                sc = opt.get("serviceClass") or ""
                sel = opt.get("selector") or ""
                # Check both serviceClass match and selector match to avoid duplicates
                if (sc == fqcn) or (sc.endswith(cls) and sel == selector):
                    exists = True
                    break
            if exists:
                continue
            
            # Find last Option element to insert after it with proper formatting
            existing_options = svc_el.findall("./Option")
            if existing_options:
                last_opt = existing_options[-1]
                # Get the tail (text after element) to preserve indentation
                # Ensure there's a newline after the closing tag
                indent_text = last_opt.tail if last_opt.tail else "\n"
                
                # Create new Option with same attribute order as existing entries
                opt = etree.Element("Option")
                opt.set("cardinality", "duplicate")
                opt.set("requestor","java.lang.Object")
                opt.set("selector", selector)
                opt.set("serviceClass", fqcn)
                # Ensure newline after the closing </Option> tag
                opt.tail = indent_text if indent_text.startswith("\n") else "\n" + indent_text
                
                # Insert after last option
                insert_idx = list(svc_el).index(last_opt) + 1
                svc_el.insert(insert_idx, opt)
            else:
                # No existing options, add with default formatting
                opt = etree.SubElement(svc_el, "Option")
                opt.set("cardinality", "duplicate")
                opt.set("requestor","java.lang.Object")
                opt.set("selector", selector)
                opt.set("serviceClass", fqcn)
                opt.tail = "\n"
            
            added.append((svc_name, fqcn))

    if not added:
        return {"ok": True, "message": "No new service entries required."}

    # Serialize while preserving original DOCTYPE and whitespace formatting
    buf = BytesIO()
    try:
        doc.write(buf, encoding="utf-8", xml_declaration=True, doctype=doc.docinfo.doctype)
        out_bytes = buf.getvalue()
        # Validate resulting XML structure (ignores DOCTYPE)
        etree.fromstring(out_bytes.split(b"\n", 2)[-1])
    except Exception as e:
        return {"ok": False, "error": f"Resulting xconf invalid: {e}"}

    if dry_run:
        return {"ok": True, "dry_run": True, "added": added}

    _atomic_write(xconf_path, out_bytes)
    return {"ok": True, "dry_run": False, "added": added, "written": xconf_path}

@mcp.tool(name="register_collection_category", description="Add a new CollectionCategory constant line")
def register_collection_category(ctx: Context, source_file: str, template_name: str, dry_run: bool = True) -> Dict[str, Any]:
    src_path = Path(source_file)
    if not src_path.exists():
        return {"ok": False, "error": f"Source not found: {source_file}"}

    md = _read_text(GH_DIR / "copilot-instructions.md")
    cfg = _parse_path_config(md)
    allowed = _allowed_prefixes_from_config(cfg)
    if not _is_allowed_write(str(src_path), allowed):
        return {"ok": False, "error": f"Write blocked: {source_file} not under allowed prefixes."}
    text = _read_text(src_path)
    line_to_add = f'    public static final CollectionCategory {template_name} = toCollectionCategory("{template_name}");\n'
    if line_to_add in text:
        return {"ok": True, "message": "Category already present."}

    anchor = text.rfind("public static final CollectionCategory")
    if anchor == -1:
        return {"ok": False, "error": "Insertion anchor not found in source."}
    insert_idx = text.find("\n", anchor) + 1
    new_text = text[:insert_idx] + line_to_add + text[insert_idx:]

    if dry_run:
        return {"ok": True, "dry_run": True, "preview_bytes": len(new_text.encode('utf-8'))}

    _atomic_write(source_file, new_text.encode("utf-8"))
    return {"ok": True, "dry_run": False, "written": source_file}

@mcp.tool(name="write_file_atomic", description="Guarded atomic write with allowlist and dry-run")
def write_file_atomic(ctx: Context, path: str, content: str, dry_run: bool = True) -> Dict[str, Any]:
    md = _read_text(GH_DIR / "copilot-instructions.md")
    cfg = _parse_path_config(md)
    allowed = _allowed_prefixes_from_config(cfg)
    if not _is_allowed_write(path, allowed):
        return {"ok": False, "error": f"Write blocked: {path} not under allowed prefixes."}
    data = content.encode("utf-8")
    if dry_run:
        return {"ok": True, "dry_run": True, "bytes": len(data)}
    _atomic_write(path, data)
    return {"ok": True, "dry_run": False, "written": path, "bytes": len(data)}

@mcp.tool(name="update_bac_generic_delete", description="Add template entry to BACGenericDeleteRecordObjInfos.xsd")
def update_bac_generic_delete(ctx: Context, template_name: str, attributes: Optional[List[str]] = None, generic_xsd_path: Optional[str] = None, dry_run: bool = True) -> Dict[str, Any]:
    md = _read_text(GH_DIR / "copilot-instructions.md")
    cfg = _parse_path_config(md)
    attrs = attributes or []
    
    # Default path: {schema_path}/BACGenericDeleteRecordObjInfos.xsd
    if not generic_xsd_path:
        schema_base = Path(cfg.bac_src_path) / "com" / "ptc" / "windchill" / "bac" / "schema"
        generic_xsd_path = str(schema_base / "BACGenericDeleteRecordObjInfos.xsd")
    
    xsd_file = Path(generic_xsd_path)
    if not xsd_file.exists():
        return {"ok": False, "error": f"XSD file not found: {generic_xsd_path}"}
    
    allowed = _allowed_prefixes_from_config(cfg)
    allowed.append(str(Path(cfg.bac_src_path) / "com" / "ptc" / "windchill" / "bac" / "schema"))
    if not _is_allowed_write(str(xsd_file), allowed):
        return {"ok": False, "error": f"Write blocked: {generic_xsd_path} not under allowed prefixes."}
    
    xml_bytes = xsd_file.read_bytes()
    try:
        parser = etree.XMLParser(remove_blank_text=False, strip_cdata=False)
        root = etree.fromstring(xml_bytes, parser=parser)
    except Exception as e:
        return {"ok": False, "error": f"Invalid XSD XML: {e}"}
    
    # Define namespace
    ns = {"xs": "http://www.w3.org/2001/XMLSchema", "bac": "http://www.ptc.com/bac/delete"}
    obj_info_name = f"{template_name}ObjInfos"
    
    # Check if complexType already exists
    existing_type = root.findall(f".//xs:complexType[@name='{obj_info_name}']", namespaces=ns)
    if existing_type:
        return {"ok": True, "message": f"ComplexType {obj_info_name} already exists in XSD."}
    
    # Step 1: Find the main BACGenericDeleteRecordObjInfos element
    main_element = root.find(".//xs:element[@name='BACGenericDeleteRecordObjInfos']", namespaces=ns)
    if main_element is None:
        return {"ok": False, "error": "BACGenericDeleteRecordObjInfos element not found."}
    
    # Find the position to insert complexType (right before the main element)
    main_elem_parent = main_element.getparent()
    main_elem_idx = list(main_elem_parent).index(main_element)
    
    # Get the tail from previous element to match formatting
    if main_elem_idx > 0:
        prev_elem = list(main_elem_parent)[main_elem_idx - 1]
        indent_tail = prev_elem.tail if prev_elem.tail else "\n  "
    else:
        indent_tail = "\n  "
    
    # Create new complexType with sequence and elements
    new_complex_type = etree.Element("{http://www.w3.org/2001/XMLSchema}complexType")
    new_complex_type.set("name", obj_info_name)
    
    if attrs:
        # Add sequence with child elements if attributes provided
        new_complex_type.text = "\n        "
        sequence = etree.SubElement(new_complex_type, "{http://www.w3.org/2001/XMLSchema}sequence")
        sequence.text = "\n            "
        sequence.tail = "\n    "
        
        for i, attr_name in enumerate(attrs):
            elem = etree.SubElement(sequence, "{http://www.w3.org/2001/XMLSchema}element")
            elem.set("name", attr_name)
            elem.set("type", "xs:string")
            elem.set("minOccurs", "0")
            elem.set("maxOccurs", "1")
            elem.tail = "\n            " if i < len(attrs) - 1 else "\n        "
    else:
        # Empty complexType if no attributes
        new_complex_type.text = "\n    "
    
    new_complex_type.tail = indent_tail
    
    # Update the previous element's tail to maintain spacing
    if main_elem_idx > 0:
        prev_elem = list(main_elem_parent)[main_elem_idx - 1]
        prev_elem.tail = indent_tail
    
    # Insert the complexType before the main element
    main_elem_parent.insert(main_elem_idx, new_complex_type)
    
    # Step 2: Add element reference in <xs:choice>
    choice = main_element.find(".//xs:choice", namespaces=ns)
    if choice is None:
        return {"ok": False, "error": "xs:choice element not found."}
    
    # Check if element already exists in choice
    existing_choice_elem = choice.findall(f".//xs:element[@name='{obj_info_name}']", namespaces=ns)
    if existing_choice_elem:
        return {"ok": True, "message": f"Element {obj_info_name} already exists in choice."}
    
    # Find last element in choice to insert after
    choice_elements = choice.findall("./xs:element", namespaces=ns)
    if choice_elements:
        last_choice_elem = choice_elements[-1]
        choice_insert_idx = list(choice).index(last_choice_elem) + 1
        # Get tail from last element to match indentation
        elem_tail = last_choice_elem.tail if last_choice_elem.tail else "\n        "
    else:
        choice_insert_idx = 0
        elem_tail = "\n        "
    
    # Create new element reference in choice
    new_choice_elem = etree.Element("{http://www.w3.org/2001/XMLSchema}element")
    new_choice_elem.set("name", obj_info_name)
    new_choice_elem.set("type", f"bac:{obj_info_name}")
    new_choice_elem.tail = elem_tail
    
    choice.insert(choice_insert_idx, new_choice_elem)
    
    out_bytes = etree.tostring(root, encoding="utf-8", xml_declaration=True)
    try:
        etree.fromstring(out_bytes)
    except Exception as e:
        return {"ok": False, "error": f"Generated XSD invalid: {e}"}
    
    if dry_run:
        return {"ok": True, "dry_run": True, "bytes": len(out_bytes)}
    
    _atomic_write(generic_xsd_path, out_bytes)
    return {"ok": True, "dry_run": False, "written": generic_xsd_path}

@mcp.tool(name="update_bac_spec", description="Add complexType (with sequence) and element entries to BACSpec.xsd")
def update_bac_spec(ctx: Context, template_name: str, attributes: Optional[List[str]] = None, bacspec_xsd_path: Optional[str] = None, dry_run: bool = True) -> Dict[str, Any]:
    md = _read_text(GH_DIR / "copilot-instructions.md")
    cfg = _parse_path_config(md)
    attrs = attributes or []
    # Enforce presence of attributes to avoid self-closing complexType and empty sequence
    if not attrs:
        return {
            "ok": False,
            "error": (
                "Attributes list is required to create a complexType with a non-empty sequence. "
                "Provide object attribute names (e.g., ['name','number'])."
            )
        }
    
    # Default path: {schema_path}/BACSpec.xsd
    if not bacspec_xsd_path:
        schema_base = Path(cfg.bac_src_path) / "com" / "ptc" / "windchill" / "bac" / "schema"
        bacspec_xsd_path = str(schema_base / "BACSpec.xsd")
    
    xsd_file = Path(bacspec_xsd_path)
    if not xsd_file.exists():
        return {"ok": False, "error": f"XSD file not found: {bacspec_xsd_path}"}
    
    allowed = _allowed_prefixes_from_config(cfg)
    allowed.append(str(Path(cfg.bac_src_path) / "com" / "ptc" / "windchill" / "bac" / "schema"))
    if not _is_allowed_write(str(xsd_file), allowed):
        return {"ok": False, "error": f"Write blocked: {bacspec_xsd_path} not under allowed prefixes."}
    
    xml_bytes = xsd_file.read_bytes()
    try:
        parser = etree.XMLParser(remove_blank_text=False, strip_cdata=False)
        root = etree.fromstring(xml_bytes, parser=parser)
    except Exception as e:
        return {"ok": False, "error": f"Invalid XSD XML: {e}"}
    
    ns = {"xs": "http://www.w3.org/2001/XMLSchema", "bac": root.get("targetNamespace", "")}
    
    # Check if complexType already exists; if so, augment it to ensure a sequence with elements
    existing_type = root.findall(f".//xs:complexType[@name='{template_name}']", namespaces=ns)
    if existing_type:
        ct = existing_type[0]
        # Ensure there's a sequence
        seq = ct.find(".//xs:sequence", namespaces=ns)
        if seq is None:
            # Make sure complexType is not self-closing by setting text for indentation
            ct.text = "\n        "
            seq = etree.SubElement(ct, "{http://www.w3.org/2001/XMLSchema}sequence")
            seq.text = "\n            "
            seq.tail = "\n    "
        
        # Collect existing element names under sequence to avoid duplicates
        existing_names = set()
        for el in seq.findall("./{http://www.w3.org/2001/XMLSchema}element"):
            n = el.get("name")
            if n:
                existing_names.add(n)

        # Append any missing attributes as xs:element
        for i, attr_name in enumerate(attrs):
            if attr_name in existing_names:
                continue
            el = etree.SubElement(seq, "{http://www.w3.org/2001/XMLSchema}element")
            el.set("name", attr_name)
            el.set("type", "xs:string")
            el.set("minOccurs", "0")
            el.set("maxOccurs", "1")
            el.tail = "\n            "

        # Ensure formatting/tail on last element and complex type
        children = seq.findall("./{http://www.w3.org/2001/XMLSchema}element")
        if children:
            for ch in children:
                ch.tail = "\n            "
            children[-1].tail = "\n        "
        if seq is not None:
            seq.tail = "\n    "
        if ct is not None and ct.getparent() is not None:
            # Preserve indentation before next sibling
            siblings = list(ct.getparent())
            try:
                idx = siblings.index(ct)
                if idx < len(siblings) - 1:
                    next_sib = siblings[idx + 1]
                    ct.tail = next_sib.tail if next_sib.tail and "\n" in next_sib.tail else "\n    "
                else:
                    ct.tail = "\n    "
            except ValueError:
                ct.tail = "\n    "

        out_bytes = etree.tostring(root, encoding="utf-8", pretty_print=True, xml_declaration=True)
        try:
            etree.fromstring(out_bytes)
        except Exception as e:
            return {"ok": False, "error": f"Generated XSD invalid: {e}"}

        if dry_run:
            return {"ok": True, "dry_run": True, "bytes": len(out_bytes)}

        _atomic_write(bacspec_xsd_path, out_bytes)
        return {"ok": True, "dry_run": False, "written": bacspec_xsd_path}
    
    # Find the BACSpec element to insert complexType before it
    bacspec_element = root.find(".//xs:element[@name='BACSpec']", namespaces=ns)
    if bacspec_element is None:
        return {"ok": False, "error": "BACSpec element not found in XSD."}
    
    parent = bacspec_element.getparent()
    bacspec_idx = list(parent).index(bacspec_element)
    
    # Get existing indentation from BACSpec element
    if bacspec_idx > 0:
        prev_elem = list(parent)[bacspec_idx - 1]
        indent = prev_elem.tail if prev_elem.tail and '\n' in prev_elem.tail else "\n    "
    else:
        indent = "\n    "
    
    # Create complexType - ensure explicit opening/closing tag with a non-empty <xs:sequence>
    complex_type = etree.Element("{http://www.w3.org/2001/XMLSchema}complexType")
    complex_type.set("name", template_name)
    
    # Add sequence with child elements (always, since attrs validated non-empty)
    complex_type.text = "\n        "
    sequence = etree.SubElement(complex_type, "{http://www.w3.org/2001/XMLSchema}sequence")
    sequence.text = "\n            "
    sequence.tail = "\n    "

    for i, attr_name in enumerate(attrs):
        elem = etree.SubElement(sequence, "{http://www.w3.org/2001/XMLSchema}element")
        elem.set("name", attr_name)
        elem.set("type", "xs:string")
        # Treat attributes as singular optional fields by default
        elem.set("minOccurs", "0")
        elem.set("maxOccurs", "1")
        elem.tail = "\n            " if i < len(attrs) - 1 else "\n        "
    
    # Set tail to match existing formatting - single newline with indent before next element
    complex_type.tail = indent
    
    # Insert the complexType before BACSpec element (this creates proper opening and closing tags)
    parent.insert(bacspec_idx, complex_type)
    
    # Now add element reference in BACSpec's sequence
    # Find the BACSpec's complexType > sequence
    bacspec_complextype = bacspec_element.find(".//xs:complexType/xs:sequence", namespaces=ns)
    if bacspec_complextype is None:
        return {"ok": False, "error": "BACSpec sequence not found."}
    
    # Check if element already exists in sequence
    existing_elem = bacspec_complextype.findall(f".//xs:element[@name='{template_name}']", namespaces=ns)
    if existing_elem:
        return {"ok": True, "message": f"Element {template_name} already exists in BACSpec sequence."}
    
    # Find last element in sequence to insert after
    sequence_elements = bacspec_complextype.findall("./xs:element", namespaces=ns)
    if sequence_elements:
        last_elem = sequence_elements[-1]
        seq_insert_idx = list(bacspec_complextype).index(last_elem) + 1
        elem_tail = "\n                "
    else:
        seq_insert_idx = 0
        elem_tail = "\n                "
    
    # Create element reference in BACSpec sequence
    new_elem = etree.Element("{http://www.w3.org/2001/XMLSchema}element")
    new_elem.set("name", template_name)
    new_elem.set("type", f"bac:{template_name}")
    new_elem.set("minOccurs", "0")
    new_elem.set("maxOccurs", "1")
    new_elem.tail = elem_tail
    
    bacspec_complextype.insert(seq_insert_idx, new_elem)
    
    out_bytes = etree.tostring(root, encoding="utf-8", pretty_print=True, xml_declaration=True)
    try:
        etree.fromstring(out_bytes)
    except Exception as e:
        return {"ok": False, "error": f"Generated XSD invalid: {e}"}
    
    if dry_run:
        return {"ok": True, "dry_run": True, "bytes": len(out_bytes)}
    
    _atomic_write(bacspec_xsd_path, out_bytes)
    return {"ok": True, "dry_run": False, "written": bacspec_xsd_path}

@mcp.tool(name="rollback_steps_2_to_12", description="Rollback artifacts generated by Steps 2–12 (dirs, registry, services, XSDs, controllers)")
def rollback_steps_2_to_12(ctx: Context, template_name: str, directory_name: str, dry_run: bool = True) -> Dict[str, Any]:
    """
    Removes outputs created during Steps 2–12 for a specific object:
    - Deletes {wt_path}/{directory_name}/bac and {test_path}/{directory_name}/bac
    - Removes <object template=...> from obj registry XML(s)
    - Removes CollectionCategory constant for the template
    - Removes <Option selector=template_name> entries in BAC-service.properties.xconf
    - Removes complexType/element for template in BACSpec.xsd
    - Removes element for template in BACGenericDeleteRecordObjInfos.xsd
    - Removes DeltaController insertion for template
    """
    md = _read_text(GH_DIR / "copilot-instructions.md")
    cfg = _parse_path_config(md)
    allowed = _allowed_prefixes_from_config(cfg)
    # Include schema and controllers folders in allowlist for modifications
    schema_dir = str(Path(cfg.bac_src_path) / "com" / "ptc" / "windchill" / "bac" / "schema")
    controllers_dir = str(Path(cfg.bac_src_path) / "com" / "ptc" / "windchill" / "bac" / "client" / "controllers")
    allowed.extend([schema_dir, controllers_dir])

    results: Dict[str, Any] = {"deleted_dirs": [], "updated_files": []}

    # Step 2: Delete directories (check contents first, report files, then remove)
    wt_bac = Path(cfg.wt_path) / directory_name / "bac"
    test_bac = Path(cfg.test_path) / directory_name / "bac"
    for d in [wt_bac, test_bac]:
        d_str = str(d)
        if _is_allowed_write(d_str, allowed) and d.exists():
            # Collect files within directory (recursive)
            files_in_dir = [str(p) for p in d.rglob("*") if p.is_file()]
            # Record check information
            results.setdefault("dir_checks", []).append({
                "dir": d_str,
                "exists": True,
                "file_count": len(files_in_dir)
            })
            if dry_run:
                results.setdefault("would_delete_dirs", []).append(d_str)
                if files_in_dir:
                    results.setdefault("would_delete_files", []).extend(files_in_dir)
            else:
                # Delete files + directory
                try:
                    shutil.rmtree(d_str, ignore_errors=True)
                finally:
                    results["deleted_dirs"].append(d_str)
                    if files_in_dir:
                        results.setdefault("deleted_files", []).extend(files_in_dir)

    # Step 3: Remove admin object from registry XML(s)
    reg_dir = Path(cfg.obj_registry_path)
    if reg_dir.exists():
        xml_files = list(reg_dir.glob("*.xml"))
        for rf in xml_files:
            rf_str = str(rf)
            if not _is_allowed_write(rf_str, allowed):
                continue
            try:
                data = rf.read_bytes()
                root = etree.fromstring(data)
            except Exception:
                continue
            changed = False
            for obj_el in root.findall(".//object"):
                if obj_el.get("template") == template_name:
                    root.remove(obj_el)
                    changed = True
            if changed:
                out = etree.tostring(root, encoding="utf-8", pretty_print=True, xml_declaration=True)
                if dry_run:
                    results.setdefault("would_update_files", []).append(rf_str)
                else:
                    _atomic_write(rf_str, out)
                    results["updated_files"].append(rf_str)

    # Step 4: Remove CollectionCategory constant
    cc_path = Path(cfg.bac_src_path) / "com" / "ptc" / "windchill" / "bac" / "CollectionCategory.java"
    cc_str = str(cc_path)
    if cc_path.exists() and _is_allowed_write(cc_str, allowed):
        text = _read_text(cc_path)
        line = f'    public static final CollectionCategory {template_name} = toCollectionCategory("{template_name}");\n'
        if line in text:
            new_text = text.replace(line, "")
            if dry_run:
                results.setdefault("would_update_files", []).append(cc_str)
            else:
                _atomic_write(cc_str, new_text.encode("utf-8"))
                results["updated_files"].append(cc_str)

    # Step 7: Remove service registrations with selector == template_name
    xconf_path = Path(cfg.service_xconf_path)
    xconf_str = str(xconf_path)
    if xconf_path.exists() and _is_allowed_write(xconf_str, allowed):
        try:
            parser = etree.XMLParser(remove_blank_text=False)
            root = etree.fromstring(xconf_path.read_bytes(), parser=parser)
        except Exception:
            root = None
        if root is not None:
            changed = False
            for svc in root.findall(".//Service"):
                to_remove = []
                for opt in svc.findall("./Option"):
                    if (opt.get("selector") or "") == template_name:
                        to_remove.append(opt)
                for opt in to_remove:
                    svc.remove(opt)
                    changed = True
            if changed:
                out = etree.tostring(root, encoding="utf-8", pretty_print=True, xml_declaration=True)
                if dry_run:
                    results.setdefault("would_update_files", []).append(xconf_str)
                else:
                    _atomic_write(xconf_str, out)
                    results["updated_files"].append(xconf_str)

    # Step 8: Remove BACSpec entries
    bacspec = Path(schema_dir) / "BACSpec.xsd"
    bacspec_str = str(bacspec)
    if bacspec.exists() and _is_allowed_write(bacspec_str, allowed):
        try:
            parser = etree.XMLParser(remove_blank_text=True)
            root = etree.fromstring(bacspec.read_bytes(), parser=parser)
            ns = {"xs": "http://www.w3.org/2001/XMLSchema"}
        except Exception:
            root = None
        if root is not None:
            changed = False
            # Remove complexType
            for ct in root.findall(f".//xs:complexType[@name='{template_name}']", namespaces=ns):
                parent = ct.getparent()
                if parent is not None:
                    parent.remove(ct)
                    changed = True
            # Remove element
            for el in root.findall(f".//xs:element[@name='{template_name}']", namespaces=ns):
                parent = el.getparent()
                if parent is not None:
                    parent.remove(el)
                    changed = True
            if changed:
                out = etree.tostring(root, encoding="utf-8", pretty_print=True, xml_declaration=True)
                if dry_run:
                    results.setdefault("would_update_files", []).append(bacspec_str)
                else:
                    _atomic_write(bacspec_str, out)
                    results["updated_files"].append(bacspec_str)

    # Step 9: Remove BACGenericDeleteRecordObjInfos element
    generic_xsd = Path(schema_dir) / "BACGenericDeleteRecordObjInfos.xsd"
    generic_str = str(generic_xsd)
    if generic_xsd.exists() and _is_allowed_write(generic_str, allowed):
        try:
            parser = etree.XMLParser(remove_blank_text=True)
            root = etree.fromstring(generic_xsd.read_bytes(), parser=parser)
            ns = {"xs": "http://www.w3.org/2001/XMLSchema"}
        except Exception:
            root = None
        if root is not None:
            changed = False
            for el in root.findall(f".//xs:element[@name='{template_name}']", namespaces=ns):
                parent = el.getparent()
                if parent is not None:
                    parent.remove(el)
                    changed = True
            if changed:
                out = etree.tostring(root, encoding="utf-8", pretty_print=True, xml_declaration=True)
                if dry_run:
                    results.setdefault("would_update_files", []).append(generic_str)
                else:
                    _atomic_write(generic_str, out)
                    results["updated_files"].append(generic_str)

    # Step 12: Remove DeltaController insertion
    # Try default controller path
    candidates = list(Path(controllers_dir).glob("*DeltaController*.java"))
    if candidates:
        ctrl_path = candidates[0]
        ctrl_str = str(ctrl_path)
        if ctrl_path.exists() and _is_allowed_write(ctrl_str, allowed):
            text = _read_text(ctrl_path)
            code = (
                f"        if ({template_name}.class.isAssignableFrom(clazz)) {{\n"
                f"            return CollectionCategory.{template_name};\n"
                f"        }}\n\n        "
            )
            if code in text:
                new_text = text.replace(code, "")
                if dry_run:
                    results.setdefault("would_update_files", []).append(ctrl_str)
                else:
                    _atomic_write(ctrl_str, new_text.encode("utf-8"))
                    results["updated_files"].append(ctrl_str)

    return {"ok": True, "dry_run": dry_run, **results}

@mcp.tool(name="register_preview_delegate", description="Register a preview delegate Option in BAC-delegates.xconf")
def register_preview_delegate(ctx: Context, service_xconf: Optional[str] = None, service_class: Optional[str] = None, selector: Optional[str] = None, dry_run: bool = True) -> Dict[str, Any]:
    """
    Register a preview delegate Option under the BACBatchPreviewDelegate Service in the provided xconf.
    If `service_xconf` is omitted the tool will use the `preview`/`preview_delegate_path` config values
    parsed from copilot-instructions.md. `service_class` should be the full FQCN of the delegate class
    (e.g. com.ptc.windchill.bac.client.delegates.preview.impl.BatchMyObjPreviewDelegate). `selector` is the
    selector string to use (typically the template name).
    """
    md = _read_text(GH_DIR / "copilot-instructions.md")
    cfg = _parse_path_config(md)

    # Determine xconf path: prefer explicit, otherwise use preview path (which in config points to directory)
    xconf_path = service_xconf or cfg.preview
    xconf_file = Path(xconf_path)
    if xconf_file.is_dir():
        # In case preview is a folder, assume file BAC-delegates.xconf inside it
        xconf_file = xconf_file / "BAC-delegates.xconf"

    if not xconf_file.exists():
        return {"ok": False, "error": f"xconf not found: {xconf_file}"}

    allowed = _allowed_prefixes_from_config(cfg)
    if not _is_allowed_write(str(xconf_file), allowed):
        return {"ok": False, "error": f"Write blocked: {xconf_file} not under allowed prefixes."}

    # Read and parse XML
    xml = xconf_file.read_bytes()
    try:
        parser = etree.XMLParser(remove_blank_text=False, strip_cdata=False)
        doc = etree.parse(BytesIO(xml), parser=parser)
        root = doc.getroot()
    except Exception as e:
        return {"ok": False, "error": f"Invalid xconf XML: {e}"}

    # Locate the preview Service by well-known name
    target_service_name = "com.ptc.windchill.bac.client.delegates.preview.BACBatchPreviewDelegate"
    svc_el = None
    for s in root.findall('.//Service'):
        if s.get("name") == target_service_name:
            svc_el = s
            break

    if svc_el is None:
        return {"ok": False, "error": f"Service element '{target_service_name}' not found in xconf."}

    # Validate inputs
    if not service_class or not selector:
        return {"ok": False, "error": "Both service_class and selector parameters are required."}

    # Check for existing Option to avoid duplicates (match by serviceClass and selector)
    for opt in svc_el.findall('./Option'):
        sc = opt.get('serviceClass') or ''
        sel = opt.get('selector') or ''
        if sc == service_class and sel == selector:
            return {"ok": True, "message": "Preview delegate option already registered."}

    # Insert new Option after last existing Option preserving formatting
    existing_options = svc_el.findall('./Option')
    if existing_options:
        last_opt = existing_options[-1]
        indent_text = last_opt.tail if last_opt.tail else "\n"
        opt = etree.Element('Option')
        opt.set('cardinality', 'duplicate')
        opt.set('requestor', 'java.lang.Object')
        opt.set('serviceClass', service_class)
        opt.set('selector', selector)
        opt.tail = indent_text if indent_text.startswith('\n') else '\n' + indent_text
        insert_idx = list(svc_el).index(last_opt) + 1
        svc_el.insert(insert_idx, opt)
    else:
        opt = etree.SubElement(svc_el, 'Option')
        opt.set('cardinality', 'duplicate')
        opt.set('requestor', 'java.lang.Object')
        opt.set('serviceClass', service_class)
        opt.set('selector', selector)
        opt.tail = '\n'

    # Serialize while preserving DOCTYPE and existing whitespace/indentation
    buf = BytesIO()
    try:
        doc.write(buf, encoding="utf-8", xml_declaration=True, doctype=doc.docinfo.doctype)
        out_bytes = buf.getvalue()
        etree.fromstring(out_bytes.split(b"\n", 2)[-1])
    except Exception as e:
        return {"ok": False, "error": f"Resulting xconf invalid: {e}"}

    if dry_run:
        return {"ok": True, "dry_run": True, "added": [(service_class, selector)]}

    _atomic_write(str(xconf_file), out_bytes)
    return {"ok": True, "dry_run": False, "added": [(service_class, selector)], "written": str(xconf_file)}

@mcp.tool(name="register_export_helper", description="Add a new object type entry to BACExportHelper.java typesXmlSpec method")
def register_export_helper(ctx: Context, template_name: str, export_helper_path: Optional[str] = None, dry_run: bool = True) -> Dict[str, Any]:
    """
    Adds a new entry to BACExportHelper.java for the specified template name.
    Inserts a line like: spec.append(typeSet.contains(CollectionCategory.{template_name}) ? "<{template_name} />" : StringUtils.EMPTY);
    before the closing </BACSpec> tag.
    """
    md = _read_text(GH_DIR / "copilot-instructions.md")
    cfg = _parse_path_config(md)
    
    # Default path: {bac_src_path}/com/ptc/windchill/bac/client/helpers/BACExportHelper.java
    if not export_helper_path:
        export_helper_path = str(Path(cfg.bac_src_path) / "com" / "ptc" / "windchill" / "bac" / "client" / "helpers" / "BACExportHelper.java")
    
    helper_file = Path(export_helper_path)
    if not helper_file.exists():
        return {"ok": False, "error": f"BACExportHelper.java not found at: {export_helper_path}"}
    
    allowed = _allowed_prefixes_from_config(cfg)
    helpers_dir = str(Path(cfg.bac_src_path) / "com" / "ptc" / "windchill" / "bac" / "client" / "helpers")
    allowed.append(helpers_dir)
    if not _is_allowed_write(str(helper_file), allowed):
        return {"ok": False, "error": f"Write blocked: {helper_file} not under allowed prefixes."}
    
    text = _read_text(helper_file)
    
    # Check if entry already exists
    new_line = f'        spec.append(typeSet.contains(CollectionCategory.{template_name}) ? "<{template_name} />" : StringUtils.EMPTY);\n'
    if new_line in text:
        return {"ok": True, "message": f"Entry for {template_name} already exists in BACExportHelper.java"}
    
    # Find the position to insert (before the closing </BACSpec> tag)
    closing_tag = '        spec.append("</BACSpec>");'
    closing_idx = text.find(closing_tag)
    if closing_idx == -1:
        return {"ok": False, "error": "Could not find closing </BACSpec> tag in BACExportHelper.java"}
    
    # Insert the new line before the closing tag
    new_text = text[:closing_idx] + new_line + text[closing_idx:]
    
    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "message": f"Would add entry for {template_name} to BACExportHelper.java",
            "insertion": new_line.strip()
        }
    
    _atomic_write(export_helper_path, new_text.encode("utf-8"))
    return {"ok": True, "dry_run": False, "written": export_helper_path, "added": template_name}


# -----------------------
# Run server
# -----------------------

if __name__ == "__main__":
    # FastMCP defaults to stdio server for MCP clients (e.g., Claude Desktop).
    # If your client needs HTTP, the Python SDK also supports other transports; stdio is recommended.
    mcp.run()
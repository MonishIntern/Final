from db import connect_db
from sqlalchemy import text

conn = connect_db()  # defaults to oracle+oracledb://urel_241:urel_241@localhost:1521/?service_name=wind12c
try:
    result = conn.execute(text("SELECT COUNT(*) FROM TeamTemplate"))
    print(list(result))
finally:
    conn.close()

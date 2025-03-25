# Keyhole_Automation_Platform\backend\mcp\tools\oracle_apex_tool.py

from fastapi import APIRouter
import oracledb
import os
from dotenv import load_dotenv
from fastapi import APIRouter

load_dotenv()

router = APIRouter(prefix="/oracle")

ORACLE_USER = "admin"
ORACLE_PASSWORD = os.getenv("ORACLE_APEX_PASSWORD")
ORACLE_HOST = "adb.us-ashburn-1.oraclecloud.com"
ORACLE_PORT = 1522
ORACLE_SERVICE_NAME = "g3c9758918c2229_keyholeinstancedatabase"

ORACLE_DSN = f"tcps://{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE_NAME}"

def get_db_connection():
    try:
        connection = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=ORACLE_DSN,
            ssl_server_dn_match=True
        )
        return connection
    except oracledb.DatabaseError as error:
        print(f"❌ Oracle DB error: {error}")
        return None

@router.get("/test")
def test_connection():
    conn = get_db_connection()
    if conn:
        conn.close()
        return {"status": "success", "message": "Database connection successful!"}
    else:
        return {"status": "error", "message": "Database connection failed."}

# config.py
import os
from dotenv import load_dotenv
from databricks.sdk import WorkspaceClient

load_dotenv()

# ----------------------------------------------------------------------
# Workspace client – **no change** required here
# ----------------------------------------------------------------------
w = WorkspaceClient(
    host=os.getenv("DATABRICKS_HOST"),
    token=os.getenv("DATABRICKS_TOKEN")
)

# ----------------------------------------------------------------------
# Genie space IDs – keep them in .env for safety
# ----------------------------------------------------------------------
SALES_SPACE_ID = os.getenv("SALES_SPACE_ID")
CUSTOMER_SPACE_ID = os.getenv("CUSTOMER_SPACE_ID")

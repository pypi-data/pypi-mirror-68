import os
from pathlib import Path


ORGSTACK_API_URL_PROD = "https://api.orgstack.io"
ORGSTACK_API_URL = os.environ.get("ORGSTACK_API_URL") or ORGSTACK_API_URL_PROD
ORGSTACK_API_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

CLI_PROGRAM_NAME = "orgstack"
CLI_COMMAND_CHOICES = ["configure", "verify"]

ORGSTACK_ENV_VAR_NAME = "ORGSTACK_ENV"
VALID_ORGSTACK_ENV_VARS = ("sandbox",)

ORGSTACK_HIDDEN_DIR_NAME = ".orgstack"
ORGSTACK_CREDENTIALS_FILE_NAME = "credentials.json"

ORGSTACK_HIDDEN_DIR_PATH = Path(
    Path.home(),
    ORGSTACK_HIDDEN_DIR_NAME
)
ORGSTACK_CREDENTIALS_FILE_PATH = Path(
    ORGSTACK_HIDDEN_DIR_PATH,
    ORGSTACK_CREDENTIALS_FILE_NAME
)

ORGSTACK_REPO_CONFIG_FILE_NAME = "orgstack.json"

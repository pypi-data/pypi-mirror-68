import sys

from . import file_utils
from ..config import settings


def credentials_exist():
    return settings.ORGSTACK_CREDENTIALS_FILE_PATH.exists()

def load_credentials():
    if credentials_exist():
        return file_utils.read_json_file(
            settings.ORGSTACK_CREDENTIALS_FILE_PATH
        )

    print(
        "OrgStack has not been configured yet.  "
        "Run 'orgstack configure' to get started."
    )
    sys.exit(1)

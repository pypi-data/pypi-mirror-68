import os
import sys
import json

from ..config import settings


def read_json_file(path):
    try:
        with open(path, "r") as in_file:
            contents = in_file.read()
    except:
        print("Unable to read file at {}".format(path))
        sys.exit(1)

    try:
        return json.loads(contents)
    except json.JSONDecodeError:
        print("Unable to parse {}.  Is this a valid JSON file?".format(path))
        sys.exit(1)

def write_json_file(path, contents):
    try:
        with open(path, "w") as out_file:
            out_file.write(json.dumps(contents))
    except:
        print("Unable to write JSON file at {}".format(path))
        sys.exit(1)

def create_orgstack_hidden_dir():
    try:
        settings.ORGSTACK_HIDDEN_DIR_PATH.mkdir()
    except FileNotFoundError:
        print("Unable to create directory {}".format(
            settings.ORGSTACK_HIDDEN_DIR_PATH
        ))
        sys.exit(1)
    except FileExistsError:
        print("Directory already exists {}".format(
            settings.ORGSTACK_HIDDEN_DIR_PATH
        ))
        sys.exit(1)

# TODO: Add support for custom orgstack.json paths
def get_repo_config_contents():
    cwd = os.getcwd()
    repo_config_file_path = "{}/{}".format(
        cwd, settings.ORGSTACK_REPO_CONFIG_FILE_NAME
    )

    if not os.path.isfile(repo_config_file_path):
        print("No {} file found in this repository".format(
            settings.ORGSTACK_REPO_CONFIG_FILE_NAME
        ))
        sys.exit(1)

    return read_json_file(repo_config_file_path)

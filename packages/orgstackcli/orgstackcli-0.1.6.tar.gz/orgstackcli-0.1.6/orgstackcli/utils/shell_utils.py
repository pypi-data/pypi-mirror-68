import sys
import subprocess
from pathlib import Path


def exec_command(command, bytes_format=False):
    try:
        output = subprocess.check_output(command.split(" "))
    except subprocess.CalledProcessError:
        print("Error while running command {}".format(command))
        sys.exit(1)

    if bytes_format:
        return output

    try:
        return output.strip().decode("utf-8")
    except UnicodeDecodeError:
        print("Unable to decode command output into UTF-8 {}".format(command))
        sys.exit(1)

def get_repo_name():
    output = exec_command("git rev-parse --show-toplevel")

    return Path(output).name

def get_repo_url():
    return exec_command("git config --get remote.origin.url")

def get_initial_commit_hash():
    return exec_command(
        "git --no-pager log --format='%H' --all --max-parents=0"
    )

def get_git_version():
    return exec_command("git --version")

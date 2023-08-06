import os
import sys

from ..config import settings


def get_orgstack_env():
    env = os.environ.get(settings.ORGSTACK_ENV_VAR_NAME)

    if env and env not in settings.VALID_ORGSTACK_ENV_VARS:
        error_msg = (
            "Invalid environment variable set for ORGSTACK_ENV: {}\n"
            "Valid options include: {}"
        ).format(env, ", ".join(settings.VALID_ORGSTACK_ENV_VARS))
        print(error_msg)
        sys.exit(1)

    return env

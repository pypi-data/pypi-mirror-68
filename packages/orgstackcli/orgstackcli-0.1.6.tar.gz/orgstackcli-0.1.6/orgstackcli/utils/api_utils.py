import sys
from urllib.parse import urlencode

import requests

from .http_utils import make_http_request
from ..config import settings


def get_api_headers(token=None):
    auth_header = {"Authorization": "Token {}".format(token)} if token else {}

    return {**settings.ORGSTACK_API_HEADERS, **auth_header}

def get_auth_token(email, password):
    url = "{}/api-token-auth/".format(settings.ORGSTACK_API_URL)
    data = {
        "username": email,
        "password": password
    }

    return make_http_request(
        url, method="POST", headers=get_api_headers(), data=data
    )

def get_team(token):
    url = "{}/v1/teams/".format(settings.ORGSTACK_API_URL)

    json_response = make_http_request(
        url=url, method="GET", headers=get_api_headers(token)
    )

    if json_response["count"] != 1:
        print("Something went wrong")
        sys.exit(1)

    return json_response["results"][0]

def get_data_source(name, version, token):
    params = {"name": name, "version": version}
    url = "{}/v1/data_sources/?{}".format(
        settings.ORGSTACK_API_URL, urlencode(params)
    )

    json_response = make_http_request(
        url=url, method="GET", headers=get_api_headers(token)
    )

    if json_response["count"] != 1:
        print("Something went wrong")
        sys.exit(1)

    return json_response["results"][0]

def get_repo_config(repo_name, initial_commit_hash, token):
    params = {
        "repo_name": repo_name,
        "initial_commit_hash": initial_commit_hash
    }
    url = "{}/v1/repo_configs/?{}".format(
        settings.ORGSTACK_API_URL, urlencode(params)
    )

    return make_http_request(
        url=url, method="GET", headers=get_api_headers(token)
    )

def create_build(data, token):
    url = "{}/v1/builds/".format(settings.ORGSTACK_API_URL)

    return make_http_request(
        url=url, method="POST", headers=get_api_headers(token), data=data
    )

def create_data_schema(data, token):
    url = "{}/v1/data_schemas/".format(settings.ORGSTACK_API_URL)
    headers = {
        "Authorization": "Token {}".format(token)
    }

    try:
        response = requests.post(url=url, headers=headers, files=data)
    except requests.exceptions.RequestException as error:
        print(str(error))
        sys.exit(1)

    return response.content

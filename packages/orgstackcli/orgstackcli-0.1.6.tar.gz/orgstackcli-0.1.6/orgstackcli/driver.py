import sys
import tempfile
import json
from getpass import getpass

from orgstackcli.utils import (
    api_utils, arg_parser_utils, file_utils, shell_utils, http_utils,
    credentials_utils, env_utils
)
from .config import settings


class CLIDriver():
    def __init__(self):
        self.orgstack_env = env_utils.get_orgstack_env()
        self.credentials_exist = credentials_utils.credentials_exist()

    def configure(self):
        if self.credentials_exist:
            print("OrgStack configuration already exists.")
            overwrite_msg = (
                "Would you like to overwrite the existing profile? [y/n]: "
            )
            overwrite = input(overwrite_msg)
            if overwrite not in ("y", "n"):
                print("Invalid response.  Exiting.")
                sys.exit(1)
            if overwrite == "n":
                print("No action taken.")
                sys.exit(0)

        print("Configuring OrgStack profile...")
        print("You will be prompted for your OrgStack email and password.")

        email = input("Enter email: ")
        password = getpass()

        print("Acquiring authentication token...")

        json_response = api_utils.get_auth_token(email, password)

        print("Writing profile to {}.".format(
            settings.ORGSTACK_CREDENTIALS_FILE_PATH
        ))

        file_utils.create_orgstack_hidden_dir()

        file_utils.write_json_file(
            settings.ORGSTACK_CREDENTIALS_FILE_PATH, json_response
        )

        print("Successfully configured OrgStack profile.")

    def update_repo_config(self):
        """
        Steps:
            1) Collect all data necessary for potential PUT/POST request
            2) Attempt to GET existing RepoConfig by filtering with params
            3) If RepoConfig exists, but config has not changed, return
               else if RepoConfig exists, and config has changed,
                   issue a PUT with new params
               else issue a POST with params
        """

        contents = credentials_utils.load_credentials()
        token = contents["token"]

        repo_name = shell_utils.get_repo_name()
        initial_commit_hash = shell_utils.get_initial_commit_hash()

        api_url = settings.ORGSTACK_API_URL

        json_response = api_utils.get_repo_config(
            repo_name, initial_commit_hash, token
        )

        # If response has no elements, RepoConfig does not exist yet

        data = {
            "repo_name": repo_name,
            "initial_commit_hash": initial_commit_hash,
            "config": file_utils.get_repo_config_contents(),
            "team": "{}/v1/teams/{}/".format(
                api_url,
                api_utils.get_team(token)["id"]
            )
        }

        if json_response["count"] == 0:
            print("This repository has not been configured yet")
            print("Creating new configuration")
            method = "POST"
            url = "{}/v1/repo_configs/".format(api_url)
        elif json_response["count"] == 1:
            print("Found existing configuration for this repository")

            # If the config property hasn't changed, return
            repo_config = json_response["results"][0]
            existing_config = repo_config["config"]
            new_config = data["config"]

            if new_config == existing_config:
                print("No update detected")
                print("No action taken")
                sys.exit(0)

            print("Updates detected")
            print("Updating configuration")
            method = "PUT"
            url = "{}/v1/repo_configs/{}/".format(api_url, repo_config["id"])

        json_response = http_utils.make_http_request(
            url=url, method=method, headers=api_utils.get_api_headers(token),
            data=data
        )

        print("Successfully updated repository")

    def verify(self):
        if self.orgstack_env != "sandbox":
            self.update_repo_config()

        repo_config_contents = file_utils.get_repo_config_contents()
        producing = repo_config_contents.get("producing")

        if producing is None:
            print("No producing definitions found")
            print("Successfully verified configuration")
            sys.exit(0)

        contents = credentials_utils.load_credentials()
        token = contents["token"]

        failed_data_sources = []

        api_url = settings.ORGSTACK_API_URL

        # Verify all producers
        for producer in producing:
            # Match producer definition to existing DataSchema
            data_source = api_utils.get_data_source(
                producer["name"], producer["version"], token
            )
            url = "{}/v1/data_sources/{}".format(api_url, data_source["id"])
            data_source = http_utils.make_http_request(
                url=url, method="GET", headers=api_utils.get_api_headers(token)
            )
            existing_data_schema = data_source.get("data_schema")

            # Ensure DataSource has a DataSchema
            if existing_data_schema is None:
                print("Data Source {} has no schema defined".format(
                    data_source["name"]
                ))
                sys.exit(1)

            # NOTE: Potentially expensive operation
            output = shell_utils.exec_command(
                producer["build_sequence"], bytes_format=True
            )

            # Create throw-away DataSchema from output
            tmp_file = tempfile.NamedTemporaryFile()
            tmp_file.write(output)
            tmp_file.seek(0)

            data = {
                "data_type": (None, existing_data_schema["data_type"], None),
                "example_data_file": (
                    tmp_file.name,
                    tmp_file.read(),
                    None
                )
            }
            new_data_schema_bytes = api_utils.create_data_schema(data, token)
            new_data_schema = json.loads(new_data_schema_bytes.decode("utf-8"))

            tmp_file.close()

            # Make sure output schema matches existing DataSource schema
            schemas_match = existing_data_schema["schema"] == new_data_schema["schema"]

            data = {
                "data_source": "{}/v1/data_sources/{}/".format(
                    api_url, data_source["id"]
                )
            }

            if schemas_match:
                message = "Generated schema matches known schema for Data Source {} {}".format(
                    data_source["name"], data_source["version"]
                )
                print(message)
                data["status"] = "pass"
            else:
                message = "Generated schema does not match known schema for Data Source {} {}".format(
                    data_source["name"], data_source["version"]
                )
                print(message)
                failed_data_sources.append("{} {}".format(data_source["name"], data_source["version"]))
                data["status"] = "fail"

            data["message"] = message
            api_utils.create_build(data, token)

        if failed_data_sources:
            print("Found Data Sources that violate schema contract: {}".format(
                ", ".join(failed_data_sources)
            ))
            sys.exit(1)

        print("All Data Sources uphold schema contract.")
        print("Finished verifying configuration.")

    def main(self):
        parser = arg_parser_utils.init_arg_parser()
        args = parser.parse_args()

        if args.command == "configure":
            self.configure()
        elif args.command == "verify":
            self.verify()

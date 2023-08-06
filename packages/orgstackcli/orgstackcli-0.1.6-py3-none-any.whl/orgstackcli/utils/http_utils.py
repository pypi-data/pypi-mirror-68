import json
import sys
import urllib
import urllib.request


def make_http_request(url, method, headers, data=None):
    if data:
        data = json.dumps(data).encode("utf-8")

    req = urllib.request.Request(
        url=url, method=method, headers=headers, data=data
    )

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as error:
        print("HTTP error: %s", error)
        sys.exit(1)
    except urllib.error.URLError as error:
        print("URL error: %s", error)
        sys.exit(1)

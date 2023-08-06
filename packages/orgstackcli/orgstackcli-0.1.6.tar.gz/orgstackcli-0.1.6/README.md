<div align="center">
  <h3>OrgStack CLI</h3>
  <i>De-risk your data pipelines</i>
</div>

### Overview
The OrgStack CLI acts as the main interface to the OrgStack platform, outside of the web application.  It is required for verifying Data Sources and producing build reports.

### Installation
###### System Dependencies
OrgStack CLI is a [Python 3](https://www.python.org/downloads/) application.  Make sure Python 3 is installed on your system.

###### Install via pip
OrgStack CLI can be installed globally (system-wide) or inside a virtualenv.
```sh
$ pip install orgstackcli
```

### Usage
Set the `ORGSTACK_ENV` environment variable to `sandbox` for local development, or leave unset for CI/CD testing:

```sh
$ export ORGSTACK_ENV=sandbox
```

Learn more about usage with the `--help` flag, and check out the official OrgStack documentation for more details.
```sh
$ orgstack --help
```

### License
This application is licensed under the Apache 2.0 license, outlined [here](/LICENSE.txt).

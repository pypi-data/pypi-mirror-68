import setuptools
from os import path


here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

install_requires = [
    "requests==2.23.0"
]


setuptools.setup(
    name="orgstackcli",
    version="0.1.6",
    author="Christian Hogan",
    author_email="christian@orgstack.io",
    packages=setuptools.find_packages(exclude=["tests*"]),
    entry_points={
        "console_scripts": [
            "orgstack = orgstackcli.orgstack:main",
        ]
    },
    url="https://pypi.org/project/orgstackcli/",
    install_requires=install_requires,
    license="Apache License 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    description="Command-line interface for the OrgStack platform",
)

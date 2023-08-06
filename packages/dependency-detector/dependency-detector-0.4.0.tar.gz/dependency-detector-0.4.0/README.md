![Python](https://github.com/meeshkan/dependency-detector/workflows/Python/badge.svg)
[![License](https://img.shields.io/pypi/l/http-types)](LICENSE)

# dependency-detector
Tool to analyse a project for packages necessary to build it.

# Installation
```sh
pip install dependency-detector
```

# Usage
Specify a directory containing a project. This will output the commands necessary to install build dependencies on a Ubuntu 20.04 environment:

```sh
$ dependency-detector tests/python37-from-pipfile 
add-apt-repository ppa:deadsnakes/ppa; apt update; apt install python3.7

$ dependency-detector tests/java8-and-maven      
apt install openjdk-8-jdk-headless; apt install maven
```

# Development
1. Create a new virtual environment.
1. Install dependencies: `pip install --upgrade -e '.[dev]'`
1. Install [pyright](https://github.com/microsoft/pyright).
1. Run `python setup.py test` to test.
1. Run `pip install dependency-detector` to install the command-line tool

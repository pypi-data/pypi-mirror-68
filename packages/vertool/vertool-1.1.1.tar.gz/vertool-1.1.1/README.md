# Project versioning controller

A small utility for a simple version of the project and maintaining their format in the right state.

## Installation

* install package via pip toolkit: `pip install vertool`
* run to get the project actual version: `vertool`

## How it work

If you are trying to get a version on a local machine, you need to get the current version of the project based on a guitar, if you do not have any tags, the program will consider that the version does not exist yet and gives you an unknown version. When trying to get the version in the pipeline, the utility will use the variable in the environment of the package, which is guaranteed to be present.

## Integration with project

To use the utility in ansible and other tools, you must call the utility in the root after which the current version of the project will be displayed on stdout:

```bash
# .
# |
# |-- .git/
# |-- apps/
#     |
#     |-- module_0
#     |-- module_1
#     ...

$ vertool
1.0.0.dev21+12345
```

To use the utility in setuptool, you must connect the module to the installation file and call the function to get the current version:

```python
from setuptools import setup
from vertool import versioning

setup(
    version=versioning.get_version(),
    // ...
)
```

## Update pip package

* Login to the PiPy repository
* Increase version in the ``vertool/__init__.py`` file
* Create a python package dist
* Update package on the PyPi repository

```bash
# Create a package dist.
python setup.py sdist bdist_wheel

# Upload package to repository.
pip install twine
twine upload -u $VT_PYPI_USERNAME -p $VT_PYPI_PASSWORD  dist/*
```

## Development

Setup git hook to linting the project before commit.

```bash
chmod a+x pre-commit && cp pre-commit .git/hooks
```

To run the test and verify the code, follow the commands below:

```bash
# To run the project linting.
flake8 vertool tests

# To run the project testing.
python -m coverage run -m unittest discover tests/
python -m coverage report -m
```

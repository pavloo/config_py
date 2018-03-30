[![Build Status](https://travis-ci.org/pavloo/config_py.svg?branch=master)](https://travis-ci.org/pavloo/config_py)

# Disclaimer: the library is under active development and not intended to be used right now

## config_py
*A Python package for managing application configurations based on [Convention Over Configuration](https://en.wikipedia.org/wiki/Convention_over_configuration) principle*.

### Installation
```
pip install config_py
```

### Basic usage
This package provides a cli for scaffolding configuration setup. Assuming you have a Python package called `my_package` given the next directory structure:
```
\-- project
    +-- my_package
    │   \-- __init__.py
    |   \-- main.py
```
If you are in `project` directory, in order to generate a configuration for `my_package`, run:
```
configpy -p my_package
```
The command above will generate a `config` package inside of `my_package`, so that directory structure looks like this after:
```
\-- project
    +-- my_package
    │   \-- __init__.py
    |   \-- main.py
    |   \-- config
    |       \-- __init__.py
    |       \-- config-dev.py
```
Now, if you import configuration in `main.py`:
```python
from .config import TEST

print(TEST)
```
and you run `main.py`, the constant `TEST` is going to be imported from `config-dev.py` (`dev` is default environment):
```
python -m my_package.main # prints TEST value imported from config-dev.py
```

#### Loading a configuration for a different environment
In order to load a new configuration for a different environment, let's name it `stage` environment, you have to create a file `config/config-stage.py`, and provide `WSGI_ENV` env variable like this:
```
WSGI_ENV=stage python -m my_package.main # prints TEST value imported from config-staging.py
```
As you can see, we imported a configuration for `stage` environment by adding a separate configuration file for that environment and without making any changes in the calling code (`main.py`).

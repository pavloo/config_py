![Library logo](logo.png)

[![Build Status](https://travis-ci.org/pavloo/config_py.svg?branch=master)](https://travis-ci.org/pavloo/config_py)

## config_py
*A Python library for managing application configurations based on [Convention Over Configuration](https://en.wikipedia.org/wiki/Convention_over_configuration) principle*.

This library is trying to solve the next problem: when you run an app in different environments (`development`, `test` etc.), you need to load different configuration parameters based on those environments. For example, you run an app in *development* with `DB_USERNAME = 'root'`, but in *production* you would like that value to be `DB_USERNAME = os.getenv('DB_USER')`.

### Notable features
1. *Convention Over Configuration*
2. It's just Python modules and packages
3. Scaffolding

### Prerequisites

* Python 3
* pip

### Installation
```
pip install configpy
```

### Basic usage
This package provides a CLI for scaffolding configuration setup. Assuming you have a Python package called `my_package` given the next directory structure:
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
    |   +-- config
    |       \-- __init__.py
    |       \-- config_dev.py
```
Let's put sample configuration value in newly created `config_dev.py`:
```
TEST='TEST'
```

Now, if you import configuration in `main.py`:
```python
from .config import TEST

print(TEST)
```
and you run `main.py`, the constant `TEST` is going to be imported from `config_dev.py` (`dev` is default environment):
```
python -m my_package.main # prints TEST value imported from config_dev.py
```

#### Adding new environment

If you want something more than default `dev` you should create new config file inside package's `config` directory:
```bash
touch {your_module}/config/config_prod.py
```

Then put the same `TEST` variable there:
```python
TEST='NOPE'
```

If you run your module with `WSGI_EVN` set to `prod` module will pick up values from this file.

#### Loading a configuration for a different environment
In order to load a new configuration for a different environment, let's name it `stage` environment, you have to create a file `config/config_stage.py`, and provide `WSGI_ENV` env variable like this:
```
WSGI_ENV=stage python -m my_package.main # prints TEST value imported from config_stage.py
```
As you can see, we imported a configuration for `stage` environment by adding a separate configuration file `config/config_stage.py` for that environment and without making any changes to the calling code.

### Root configuration package
There is a use case when you may want to have a root configuration package, and share that configuration between other packages at the root level (and those packages may have their own configurations as well). Given the next directory structure:
```
\-- project
    +-- my_package
    │   \-- __init__.py
    |   \-- main.py
    |   +-- config
    +-- my_package1
    │   \-- __init__.py
    |   \-- main.py
```
in `project` directory run:
```
configpy
```
It will result in creating root `config` module:
```
\-- project
    +-- my_package
    │   \-- __init__.py
    |   \-- main.py
    |   +-- config
    +-- my_package1
    │   \-- __init__.py
    |   \-- main.py
    +-- config
    |   \-- __init__.py
    |   \-- config_dev.py
```
Both `my_package/main.py` and `my_package1/main.py` can import this config like this
```
from config import TEST

print(TEST)
```
and running `python -m my_package.main` and `python -m my_package1.main` respectively will print a value of `TEST` from `config_dev.py` (default config file as described in **Basic usage**).

### Other options
In order to get a list of other available options, run:
```
configpy -h
```

If you want to use different name of ENV_VAR providing environment setup (`dev`, `stage`...) than `WSGI_ENV` you can use `-e` or `--env_var` option while generating config:
```
configpy -p my_module -e NAME_OF_ENVIRONMENT_VAR
```
### License
This project is licensed under the [MIT License](LICENSE).

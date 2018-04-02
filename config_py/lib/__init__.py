import os
import importlib
import re
import logging


def get_environment(env_var_name):
    return os.getenv(env_var_name, 'dev')


class ENV(object):

    def __init__(self, env):
        self.env = env

    @property
    def name(self):
        return self.env

    def __getattr__(self, name):

        if not re.compile('is_\w+').match(name):
            raise AttributeError('No attribute with name: {}'.format(name))

        def _missing(*args, **kwargs):
            _, asserted_env = name.split('_')
            return asserted_env == self.env

        return _missing


def import_config(glob, **kwargs):
    package = kwargs.get('package', '')
    env_var_name = kwargs.get('env_var', 'WSGI_ENV')
    env = get_environment(env_var_name)

    conf_module = '.config_{}'.format(env)
    conf_package = '{}config'.format(package)
    try:
        my_module = importlib.import_module(
            conf_module,
            conf_package
        )
    except ModuleNotFoundError:
        logging.warning('There is no configuration module for environment "{}"'.format(env))
        logging.warning(
            'Expected module to be present "{}{}"'.format(conf_package, conf_module)
        )
        return

    module_dict = my_module.__dict__
    try:
        to_import = my_module.__all__
    except AttributeError:
        to_import = [name for name in module_dict if not name.startswith('_')]

    d = {name: module_dict[name] for name in to_import}
    d['env'] = ENV(env)

    glob.update(d)

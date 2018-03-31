import os
import importlib
import re


def get_environment():
    return os.getenv('WSGI_ENV', 'dev')


def import_config(glob, package=''):
    env = get_environment()

    my_module = importlib.import_module(
        '.config-{}'.format(env),
        '{}config'.format(package)
    )
    module_dict = my_module.__dict__
    try:
        to_import = my_module.__all__
    except AttributeError:
        to_import = [name for name in module_dict if not name.startswith('_')]
    glob.update({name: module_dict[name] for name in to_import})


class ENV(object):

    @property
    def name(self):
        return get_environment()

    def __getattr__(self, name):

        if not re.compile('is_\w+').match(name):
            raise AttributeError('No attribute with name: {}'.format(name))

        def _missing(*args, **kwargs):
            env = get_environment()
            _, asserted_env = name.split('_')
            return asserted_env == env

        return _missing


def import_config(glob, package=''):
    env = get_environment()

    my_module = importlib.import_module(
        '.config-{}'.format(env),
        '{}config'.format(package)
    )
    module_dict = my_module.__dict__
    try:
        to_import = my_module.__all__
    except AttributeError:
        to_import = [name for name in module_dict if not name.startswith('_')]

    env = ENV()
    d = {name: module_dict[name] for name in to_import}
    d['env'] = ENV()

    glob.update(d)

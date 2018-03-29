import os
import importlib

def import_config(glob, package=''):
    WSGI_ENV = os.getenv('WSGI_ENV', 'dev')

    my_module = importlib.import_module(
        '.config-{}'.format(WSGI_ENV),
        '{}config'.format(package)
    )
    module_dict = my_module.__dict__
    try:
        to_import = my_module.__all__
    except AttributeError:
        to_import = [name for name in module_dict if not name.startswith('_')]
    glob.update({name: module_dict[name] for name in to_import})

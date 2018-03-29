#!/usr/bin/env python
import click
import os
import shutil


CONF_DIR_NAME = 'config'
DEV_FILE = 'config-dev.py'
ERROR_ALREADY_EXISTS_FMT = '"config" module already exists for the {} module'
ROOT_SRC_DIR = os.path.dirname(os.path.realpath(__file__)) + '/../fixtures/root/'
MODULE_SRC_DIR = os.path.dirname(os.path.realpath(__file__)) + '/../fixtures/module/'


def generate_root_config():
    src_dir = ROOT_SRC_DIR
    conf_dir = os.getcwd() + '/' + CONF_DIR_NAME
    if not os.path.exists(conf_dir):
        os.makedirs(conf_dir)
        shutil.copy2(src_dir + '__init__.py', conf_dir)
        shutil.copy2(src_dir + DEV_FILE, conf_dir)
        return

    click.secho(
        ERROR_ALREADY_EXISTS_FMT.format('root'),
        err=True,
        fg='red'
    )


def generate_module_config(module):
    src_dir = MODULE_SRC_DIR
    conf_dir = os.getcwd() + '/' + '/'.join(module.split('.')) + '/' + CONF_DIR_NAME + '/'
    if os.path.exists(conf_dir):
        click.secho(
            ERROR_ALREADY_EXISTS_FMT.format('"{}"'.format(module)),
            err=True,
            fg='red'
        )
        return

    os.makedirs(conf_dir)
    src_init_fmt = open(src_dir + '__init__.py').read()
    dest_init_f = open(conf_dir + '__init__.py', 'w+')
    dest_init_f.write(src_init_fmt.format(module=module))
    shutil.copy2(src_dir + DEV_FILE, conf_dir)


@click.command()
@click.option("-m", "--module", help="module to create a config for", default=None)
def config_py(module):
    if not module:
        generate_root_config()
        return

    generate_module_config(module)


if __name__ == "__main__":
    config_py()

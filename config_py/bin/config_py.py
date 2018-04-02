#!/usr/bin/env python
import click
import os
import shutil
import sys

CONF_DIR_NAME = 'config'
DEV_FILE = 'config_dev.py'
INFO_GENERATING_FMT = 'Generating "config" package for the {} package...'
ERROR_ALREADY_EXISTS_FMT = '"config" package already exists for the {} package'
ROOT_SRC_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '..', 'fixtures', 'root'
)
PACKAGE_SRC_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '..', 'fixtures', 'package'
)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

with open(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '..', '..', 'version.py'
)) as f:
    exec(f.read())


def generate_root_config(env_var_name):
    src_dir = ROOT_SRC_DIR
    conf_dir = os.path.join(os.getcwd(), CONF_DIR_NAME)
    if not os.path.exists(conf_dir):
        os.makedirs(conf_dir)
        shutil.copy2(os.path.join(src_dir, '__init__.py'), conf_dir)
        shutil.copy2(os.path.join(src_dir, DEV_FILE), conf_dir)
        return

    click.secho(
        ERROR_ALREADY_EXISTS_FMT.format('root'),
        err=True,
        fg='red'
    )
    sys.exit(1)


def generate_package_config(package):
    src_dir = PACKAGE_SRC_DIR
    conf_dir = os.path.join(os.getcwd(), *package.split('.'), CONF_DIR_NAME)
    if os.path.exists(conf_dir):
        click.secho(
            ERROR_ALREADY_EXISTS_FMT.format('"{}"'.format(package)),
            err=True,
            fg='red'
        )
        sys.exit(1)

    os.makedirs(conf_dir)
    with open(os.path.join(src_dir, '__init__.py'), 'r') as src_init, \
            open(os.path.join(conf_dir, '__init__.py'), 'w+') as dest_init_f:  # nopep8
        src_init_fmt = src_init.read()
        dest_init_f.write(src_init_fmt.format(package=package))
    shutil.copy2(os.path.join(src_dir, DEV_FILE), conf_dir)


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("-p", "--package", help="python package to create a config for", default=None)
@click.option(
    "-e",
    "--env_var",
    help="env variable to get the name of environment from",
    default='WSGI_ENV'
)
@click.option('-v', '--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True, help="shows library version")
def config_py(package, env_var):
    click.echo(INFO_GENERATING_FMT.format('"{}"'.format(package) if package else 'root'))

    if package:
        generate_package_config(package)
    else:
        generate_root_config(env_var)

    click.secho(
        'Success!',
        err=True,
        fg='green'
    )


if __name__ == "__main__":
    config_py()

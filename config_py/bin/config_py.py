#!/usr/bin/env python
import click
import os
import shutil
import sys

CONF_DIR_NAME = 'config'
DEV_FILE = 'config_dev.py'
INFO_GENERATING_FMT = 'Generating "config" package for the {} package...'
ERROR_ALREADY_EXISTS_FMT = '"config" package already exists for the {} package'
SRC_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '..', 'fixtures'
)
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

with open(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '..', '..', 'version', '__init__.py'
)) as f:
    exec(f.read())


def generate_config(arguments_str, package):
    src_dir = SRC_DIR
    if package:
        conf_dir = os.path.join(os.getcwd(), *package.split('.'), CONF_DIR_NAME)
    else:
        conf_dir = os.path.join(os.getcwd(), CONF_DIR_NAME)
    if os.path.exists(conf_dir):
        click.secho(
            ERROR_ALREADY_EXISTS_FMT.format('"{}"'.format(package) if package else 'root'),
            err=True,
            fg='red'
        )
        sys.exit(1)

    click.echo('Generating config at {}'.format(conf_dir))

    os.makedirs(conf_dir)
    with open(os.path.join(src_dir, '__init__.py'), 'r') as src_init, \
            open(os.path.join(conf_dir, '__init__.py'), 'w+') as dest_init_f:  # nopep8
        click.echo('Setting __init__ file at {}'.format(os.path.join(conf_dir, '__init__.py')))
        src_init_fmt = src_init.read()
        dest_init_f.write(src_init_fmt.format(arguments_str=arguments_str))

    click.echo('Creating config_dev at {}'.format(os.path.join(conf_dir, DEV_FILE)))
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

    arguments_str = ''
    if package:
        arguments_str += ", package='{}.'".format(package)
    if env_var:
        arguments_str += ", env_var='{}'".format(env_var)

    generate_config(arguments_str, package)

    click.secho(
        'Success!',
        err=True,
        fg='green'
    )


if __name__ == "__main__":
    config_py()

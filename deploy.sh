#!/usr/bin/env bash

echo 'Building a wheel'
python setup.py bdist_wheel
echo 'Deploying to PyPI'
twine upload -u $PYPI_USERNAME -p $PYPI_PASSWORD dist/*

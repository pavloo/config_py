#!/usr/bin/env bash

pip install twine
python setup.py bdist_wheel
twine upload -u $PYPI_USERNAME -p $PYPI_PASSWORD dist/*

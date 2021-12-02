#!/usr/bin/env bash
set -e

# run tests
python3 test.py

python3 setup.py sdist bdist_wheel
pip3 install --user --force-reinstall dist/icc-1.0-py3-none-any.whl


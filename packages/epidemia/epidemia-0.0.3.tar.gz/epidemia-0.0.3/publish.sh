#!/usr/bin/sh
set -e

mkdir -p dist
rm dist/* || true

python setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*

#!/bin/bash
rm -r dist/ build/ .eggs/
python setup.py sdist bdist_wheel
python -m twine upload -s dist/*

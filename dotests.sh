#!/usr/bin/env bash

echo 'Core tests:'
pytest --ignore='Developer Testing' --ignore-glob='*test_preparser.py'
echo 'Doc tests:'
pytest --ignore='tests' --ignore='Developer Testing' --ignore-glob='*old*'  --doctest-modules
echo 'Preparser tests:'
ipython -m pytest tests/test_preparser.py
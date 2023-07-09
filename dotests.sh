#!/usr/bin/env bash

echo 'Core tests:'
pytest --ignore='Developer Testing' --ignore-glob='*test_preparser.py' --ignore-glob='*test_numerics.py'
echo 'Doc tests:'
pytest --ignore='tests' --ignore='Developer Testing' --ignore-glob='*old*'  --doctest-modules
echo 'Preparser and numerics tests (require ipython environment):'
ipython -m pytest tests/test_preparser.py tests/test_numerics.py
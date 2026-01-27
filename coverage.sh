#!/usr/bin/env bash

echo "Core coverage:"
pytest --cov=algebra_with_sympy tests/test_util.py
pytest --cov=algebra_with_sympy --cov-append tests/test_algebraic_equation.py
pytest --cov=algebra_with_sympy --cov-append tests/test_extension_of_sympy_functions.py
echo "Doc test"
pytest --doctest-modules --cov=algebra_with_sympy --cov-append algebra_with_sympy/algebraic_equation.py
#echo "Preparser and numerics tests (require ipython environment):"
#ipython -m pytest --cov=algebra_with_sympy --cov-append tests/test_preparser.py tests/test_numerics.py
#ipython -m pytest --cov=algebra_with_sympy --cov-append tests/test_preparser.py tests/test_numerics.py

#coverage report

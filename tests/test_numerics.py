#!ipython

from algebra_with_sympy.preparser import integers_as_exact
from algebra_with_sympy.algebraic_equation import set_integers_as_exact, \
    unset_integers_as_exact, algwsym_config
from IPython import get_ipython
from pytest import raises

if not(get_ipython()):
    raise EnvironmentError('This test module file must be run in an ipython '
                           'environment. Use `ipython -m pytest path-to-file`.'
                           ' To avoid running this file in a general test '
                           'use `pytest --ignore-glob="*test_numerics.py"`')

# Set up the global config object
get_ipython().user_ns['algwsym_config'] = algwsym_config
def test_set_integers_as_exact():
    set_integers_as_exact()
    assert integers_as_exact in get_ipython().input_transformers_post
    assert algwsym_config.numerics.integers_as_exact == True

def test_integers_as_exact():
    from sympy.core.symbol import symbols
    import __main__ as userns
    setattr(userns, 'x', symbols('x'))
    setattr(userns, 'y', symbols('y'))
    setattr(userns, 'z', symbols('z'))
    lines = []
    lines.append('1/2*x + 0.333*x')
    lines.append('2/3*z + 2.0*y + ln(3*x)')
    result = integers_as_exact(lines)
    splitlines = result.split('\n')
    expectedlines = ['Integer (1 )/Integer (2 )*x +0.333 *x ',
            'Integer (2 )/Integer (3 )*z +2.0 *y +ln (Integer (3 )*x )']
    for k in range(len(splitlines)):
        assert splitlines[k] == expectedlines[k]
    delattr(userns, 'x')
    delattr(userns, 'y')
    delattr(userns, 'z')

def test_unset_integers_as_exact():
    unset_integers_as_exact()
    assert algwsym_config.numerics.integers_as_exact == False
    assert integers_as_exact not in get_ipython().input_transformers_post

#!ipython
from algebra_with_sympy.preparser import algebra_with_sympy_preparser as parser
from algebra_with_sympy.preparser import integers_as_exact
from IPython import get_ipython
from pytest import raises

if not(get_ipython()):
    raise EnvironmentError('This test module file must be run in an ipython '
                           'environment. Use `ipython -m pytest path-to-file`.'
                           ' To avoid running this file in a general test '
                           'use `pytest --ignore-glob="*testpreparser.py"`')

def test_install_preparser():
    assert(get_ipython())
    get_ipython().input_transformers_post.append(parser)

def test_parsing():
    lines = []
    expected_out = []
    lines.append('# A comment.\n')
    expected_out.append('# A comment.\n')
    assert parser(lines) == expected_out
    lines.append('eq1 =@ a + b = c/d\n')
    expected_out.append('eq1 = Eqn( a + b , c/d)\n')
    assert parser(lines) == expected_out
    lines.append('obj?\n')
    expected_out.append('obj?\n')
    assert parser(lines) == expected_out
    lines.append('eq1 =@a + b=c/d\n')
    expected_out.append('eq1 = Eqn(a + b,c/d)\n')
    assert parser(lines) == expected_out
    lines.append('tst = (a\n')
    expected_out.append('tst = (a\n')
    lines.append('      +b)\n')
    expected_out.append('      +b)\n')
    assert parser(lines) == expected_out
    lines.append('@property\n')
    expected_out.append('@property\n')
    assert parser(lines) == expected_out
    lines.append('\n')
    expected_out.append('\n')
    assert parser(lines) == expected_out
    lines.append('eq1 =@ a + b = c/d # A trailing comment\n')
    expected_out.append('eq1 = Eqn( a + b , c/d )\n')
    assert parser(lines) == expected_out

def test_parsing_errors():
    lines = []
    expected_out = []
    lines.append('# A comment.\n')
    expected_out.append('# A comment.\n')
    assert parser(lines) == expected_out
    lines.append('eq1 =@ a + b > c/d\n')
    raises(ValueError, lambda: parser(lines))

def test_integers_as_exact():
    lines = []
    lines.append('1/2*x + 0.333*x')
    lines.append('2/3*z + 2.0*y + ln(3*x)')
    result = integers_as_exact(lines)
    splitlines = result.split('\n')
    expectedlines = ['Integer (1 )/Integer (2 )*x +0.333 *x ',
            'Integer (2 )/Integer (3 )*z +2.0 *y +ln (Integer (3 )*x )']
    for k in range(len(splitlines)):
        assert splitlines[k] == expectedlines[k]
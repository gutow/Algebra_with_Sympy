#!ipython
from algebra_with_sympy.preparser import algebra_with_sympy_preparser as parser
from IPython import get_ipython

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

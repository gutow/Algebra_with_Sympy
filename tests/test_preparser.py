#!ipython
from algebra_with_sympy.preparser import algebra_with_sympy_preparser as parser
from algebra_with_sympy.preparser import integers_as_exact, toIntegerInSympyExpr
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

def test_toIntegerInSympyExpr():
    from sympy.core.symbol import symbols
    import __main__ as userns
    setattr(userns,'a', symbols('a'))
    setattr(userns, 'b', symbols('b'))
    setattr(userns, 'c', symbols('c'))
    setattr(userns, 'x', symbols('x'))
    tststr ='z, d = symbols(\'z d\')\n'
    tststr +='DG = Symbol("\Delta G")\n'
    tststr += 'units("kg m s")\n'
    tststr += 'eq1 = Eqn(a*x**2 + b*x + c,\n'
    tststr += '0)\n'
    tststr += 's = 2*m/(3*s)\n'
    tststr += 'o = z+2/3*d\n'
    tststr += 'p = 2\n'
    tststr += 'n = 3.0\n'
    tststr += 'r = 2/3*p\n'
    tststr += 'l = 3*p + 3/4*d\n'
    tststr += 'k = 3*p + 3/4*n\n'
    tststr += 'y = [1, 2.0, 4, 5.6]\n'
    tststr += 'f = DG*5/2 + s\n'
    resultstr = 'z ,d =symbols (\'z d\')\n'
    resultstr += 'DG =Symbol ("\\Delta G")\n'
    resultstr += 'units ("kg m s")\n'
    resultstr += 'eq1 =Eqn (a *x **Integer (2 )+b *x +c ,\n'
    resultstr += 'Integer (0 ))\n'
    resultstr += 's =Integer (2 )*m /(Integer (3 )*s )\n'
    resultstr += 'o =z +Integer (2 )/Integer (3 )*d \n'
    resultstr += 'p =2 \n'
    resultstr += 'n =3.0 \n'
    resultstr += 'r =2 /3 *p \n'
    resultstr += 'l =Integer (3 )*p +Integer (3 )/Integer (4 )*d \n'
    resultstr += 'k =3 *p +3 /4 *n \n'
    resultstr += 'y =[1 ,2.0 ,4 ,5.6 ]\n'
    resultstr += 'f =DG *Integer (5 )/Integer (2 )+s \n'
    assert toIntegerInSympyExpr(tststr) == resultstr
    #cleanup
    delattr(userns,'a')
    delattr(userns, 'b')
    delattr(userns, 'c')
    delattr(userns, 'x')

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
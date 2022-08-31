from sympy import symbols, integrate, simplify, expand, factor, Integral, Add
from sympy import diff, FiniteSet, Equality, Function, functions, Matrix, S
from sympy import sin, cos, log, exp, latex, Symbol
from sympy.core.function import AppliedUndef
from sympy.printing.latex import LatexPrinter
from algebra_with_sympy.algebraic_equation import solve, collect, Equation, Eqn, sqrt, root
from algebra_with_sympy.algebraic_equation import algwsym_config
from algebra_with_sympy.algebraic_equation import EqnFunction, str_to_extend_sympy_func
from algebra_with_sympy.algebraic_equation import _skip_

from pytest import raises

def test_str_to_extend_sympy_func():
    teststr = 'testname'
    execstr = 'class %S(%S,EqnFunction):\n    pass\n'
    execstr = execstr.replace('%S',str(teststr))
    assert str_to_extend_sympy_func(teststr)==execstr
    pass

#####
# Extension just the functions used for testing
#####

for func in ('sin', 'cos', 'log', 'exp'):
    if func not in _skip_:
        try:
            exec(str_to_extend_sympy_func(func), globals(), locals())
        except TypeError:
            from warnings import warn
            warn('SymPy function/operation ' + str(func) + ' may not work ' \
                'properly with Equations. If you use it with Equations, ' \
                'validate its behavior. We are working to address this ' \
                'issue.')


class CustomLatexPrinter(LatexPrinter):
    """Print undefined applied functions without arguments"""
    def _print_Function(self, expr, exp=None):
        if isinstance(expr, AppliedUndef):
            return self._print(Symbol(expr.func.__name__))
        return super()._print_Function(expr, exp)


def my_latex(expr, **settings):
    """Mimic latex()"""
    return CustomLatexPrinter(settings).doprint(expr)


def test_define_equation():
    a, b, c = symbols('a b c')
    raises(TypeError, lambda: Equation(FiniteSet(a), FiniteSet(b, c)))
    assert(Equation(1, 0).check() == False)
    assert Eqn(1, 0) == Equation(1, 0)
    tsteqn = Equation(a, b/c)
    assert tsteqn.args == (a, b/c)
    assert tsteqn.lhs == a
    assert tsteqn.rhs == b/c
    assert tsteqn.free_symbols == {a, b, c}


def test_convert_equation():
    a, b, c = symbols('a b c')
    tsteqn = Equation(a, b/c)
    assert tsteqn.as_Boolean() == Equality(a, b/c)
    assert tsteqn.reversed == Equation(b/c, a)
    assert tsteqn.swap == Equation(b/c, a)


def test_binary_op():
    a, b, c = symbols('a b c')
    tsteqn = Equation(a, b/c)
    assert tsteqn + c == Equation(a + c, b/c + c)
    assert c + tsteqn == Equation(c + a, c + b/c)
    assert tsteqn*c == Equation(a*c, b)
    assert c*tsteqn == Equation(c*a, b)
    assert tsteqn - c == Equation(a - c, b/c - c)
    assert c - tsteqn == Equation(c - a, c - b/c)
    assert tsteqn/ c == Equation(a/c, b/c**2)
    assert c/tsteqn == Equation(c/a, c**2/b)
    assert tsteqn % c == Equation(a % c, (b/c) % c)
    assert c % tsteqn == Equation(c % a, c % (b/c))
    assert tsteqn**c == Equation(a**c, (b/c)**c)
    assert c**tsteqn == Equation(c**a, c**(b/c))
    assert tsteqn + tsteqn == Equation(2*a, 2*b/c)
    assert tsteqn*tsteqn == Equation(a**2, b**2/c**2)
    assert tsteqn - tsteqn == Equation(0, 0)
    assert tsteqn/tsteqn == Equation(1, 1)
    assert tsteqn % tsteqn == Equation(0, 0)
    assert tsteqn**tsteqn == Equation(a**a, (b/c)**(b/c))


def test_outputs():
    algwsym_config.output.show_code = False
    # True for above not tested as it sends output to standard out via
    # `print()`.
    algwsym_config.output.human_text = False
    a, b, c = symbols('a b c')
    tsteqn = Eqn(a, b/c)
    assert tsteqn.__repr__() == 'Equation(a, b/c)'
    algwsym_config.output.human_text = True
    assert tsteqn.__repr__() == 'a = b/c'
    assert tsteqn.__str__() == 'a = b/c'
    assert latex(tsteqn) == 'a=\\frac{b}{c}'

    f = Function("f")(a, b, c)
    eq = Eqn(f, 2)
    assert latex(eq) == "f{\\left(a,b,c \\right)}=2"
    # use custom printer
    assert my_latex(eq) == "f=2"


def test_sympy_functions():
    a, b, c = symbols('a b c')
    tsteqn = Equation(a, b/c)
    assert sin(tsteqn) == Equation(sin(a),sin(b/c))
    assert log(tsteqn) == Equation(log(a),log(b/c))
    # Check matrix exponentiation is not overridden.
    assert exp(tsteqn) == Equation(exp(tsteqn.lhs),exp(tsteqn.rhs))
    tsteqn5 = Equation(a, Matrix([[1, 1], [1, 1]]))
    assert exp(tsteqn5).lhs == exp(a)
    assert exp(tsteqn5).rhs == exp(Matrix([[1, 1], [1, 1]]))

def test_helper_functions():
    a, b, c, x= symbols('a b c x')
    tsteqn = Equation(a, b/c)
    raises(ValueError, lambda: integrate(tsteqn, c))
    raises(AttributeError, lambda: integrate(tsteqn, c, side='right'))
    assert tsteqn.evalf(4, {b: 2.0, c: 4}) == Equation(a, 0.5000)
    assert diff(tsteqn, c) == Equation(diff(a, c, evaluate=False), -b/c**2)
    tsteqn = Equation(a*c, b/c)
    assert diff(tsteqn, c) == Equation(a, -b/c**2)
    assert integrate(tsteqn, c, side='rhs') == integrate(tsteqn.rhs, c)
    assert integrate(tsteqn, c, side='lhs') == integrate(tsteqn.lhs, c)

    def adsq(eqn):
        # Arbitrary python function
        return eqn + eqn**2

    assert adsq(Equation(a*c, b/c)) == Equation(a**2*c**2 + a*c, b**2/c**2 +
                                                b/c)
    assert Equation((a - 1)*(a + 1), (2*b + c)**2).expand() == Equation(
        a**2 - 1, 4*b**2 + 4*b*c + c**2)
    assert expand(Equation((a - 1)*(a + 1), (2*b + c)**2)) == Equation(
        a**2 - 1, 4*b**2 + 4*b*c + c**2)
    assert Equation(a**2 - 1, 4*b**2 + 4*b*c + c**2).factor() == Equation(
        (a - 1)*(a + 1), (2*b + c)**2)
    assert factor(Equation(a**2 - 1, 4*b**2 + 4*b*c + c**2)) == Equation(
        (a - 1)*(a + 1), (2*b + c)**2)
    assert Equation(a**2 - 1, 4*b**2 + 4*b*c + c*a).collect(c) == Equation(
        a**2- 1, 4*b**2 + c*(a + 4*b))
    assert collect(Equation(a**2 - 1, 4*b**2 + 4*b*c + c*a), c) == Equation(
        a**2- 1, 4*b**2 + c*(a + 4*b))
    assert Equation((a + 1)**2/(a + 1), exp(log(c))).simplify() == Equation(
        a + 1, c)
    assert simplify(Equation((a + 1)**2/(a + 1), exp(log(c)))) == Equation(
        a + 1, c)
    assert Equation(x, ((b - sqrt(4*a*c + b**2))/(2*a)).expand()) in solve(
        Equation(a*x**2,b*x+c),x)
    assert Equation(x, ((b + sqrt(4*a*c + b**2))/(2*a)).expand()) in solve(
        Equation(a*x**2,b*x+c),x)
    assert len(solve(Equation(a*x**2,b*x+c), x)) == 2
    assert root(Eqn(a,b/c),3) == Equation(a**(S(1)/S(3)), (b/c)**(S(1)/S(3)))
    assert sqrt(Eqn(a,b/c)) == Equation(sqrt(a), sqrt(b/c))


def test_apply_syntax():
    a, b, c, x = symbols('a b c x')
    tsteqn = Equation(a, b/c)
    assert tsteqn.apply(log) == Equation(log(a), log(b/c))
    assert tsteqn.applylhs(log) == Equation(log(a), b / c)
    assert tsteqn.applyrhs(log) == Equation(a, log(b / c))
    poly = Equation(a*x**2 + b*x + c*x**2, a*x**3 + b*x**3 + c*x)
    assert poly.applyrhs(collect, x) == Equation(poly.lhs, poly.rhs.collect(x))


def test_do_syntax():
    a, b, c, x = symbols('a b c x')
    tsteqn = Equation(a, b/c)
    raises(AttributeError, lambda: tsteqn.do.log())
    poly = Equation(a*x**2 + b*x + c*x**2, a*x**3 + b*x**3 + c*x)
    assert poly.dorhs.collect(x) == Eqn(poly.lhs, poly.rhs.collect(x))
    assert poly.dolhs.collect(x) == Eqn(poly.lhs.collect(x), poly.rhs)
    assert poly.do.collect(x) == Eqn(poly.lhs.collect(x), poly.rhs.collect(x))


def test_subs():
    a, b, c, x = symbols('a b c x')
    eq1 = Equation(x + a + b + c, x * a * b * c)
    eq2 = Equation(x + a, 4)
    assert eq1.subs(a, 2) == Equation(x + b + c + 2, 2 * x * b * c)
    assert eq1.subs([(a, 2), (b, 3)]) == Equation(x + c + 5, 6 * x * c)
    assert eq1.subs({a: 2, b: 3}) == Equation(x + c + 5, 6 * x * c)
    assert eq1.subs(eq2) == Equation(4 + b + c, x * a * b * c)

    # verify that proper errors are raised
    eq3 = Equation(b, 5)
    raises(TypeError, lambda: eq1.subs([eq2, eq3]))
    raises(ValueError, lambda: eq1.subs(eq2, {b: 5}))

    # verify that substituting an Equation into an expression is not supported
    raises(ValueError, lambda: eq1.dolhs.subs(eq2))
    raises(ValueError, lambda: eq1.dorhs.subs(eq2))
    raises(ValueError, lambda: (x + a + b + c).subs(eq2))

    # verify the effectivness of `simultaneous`
    eq = Equation((x + a) / a, b * c)
    sd = {x + a: a, a: x + a}
    assert eq.subs(sd) == Equation(1, b * c)
    assert eq.subs(sd, simultaneous=True) == Equation(a / (x + a), b * c)

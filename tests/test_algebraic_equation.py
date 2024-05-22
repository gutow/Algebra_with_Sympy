from sympy import symbols, integrate, simplify, expand, factor, Integral, Add
from sympy import diff, FiniteSet, Equation, Function, Matrix, S, Eq
from sympy import sin, cos, log, exp, latex, Symbol, I, pi
from sympy.core.function import AppliedUndef
from sympy.printing.latex import LatexPrinter
from algebra_with_sympy.algebraic_equation import solve, collect
from algebra_with_sympy.algebraic_equation import Equality, units
from sympy import Eqn, sqrt, root, Heaviside
from algebra_with_sympy.algebraic_equation import algwsym_config


from pytest import raises

#####
# Testing that sympy functions work with Equations
#####

# Overridden elsewhere
_extended_ = ('sqrt', 'cbrt', 'root')

# Either not applicable to Equations or have not yet figured out a way
# to systematically apply to an Equation.
# TODO examine these more carefully (top priority: real_root, Ynm_c).
_not_applicable_to_equations_ = ('Min', 'Max', 'Id', 'real_root',
        'unbranched_argument', 'polarify', 'unpolarify',
        'piecewise_fold', 'E1', 'Eijk', 'bspline_basis',
        'bspline_basis_set', 'interpolating_spline', 'jn_zeros',
        'jacobi_normalized', 'Ynm_c', 'piecewise_exclusive', 'Piecewise',
        'motzkin', 'hyper','meijerg', 'chebyshevu_root', 'chebyshevt_root',
        'betainc_regularized')
_skip_ = _extended_ + _not_applicable_to_equations_

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
    assert tsteqn.as_Boolean() == Eq(a, b/c)
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
    assert tsteqn**a == Equation(a**a, (b/c)**a)
    assert tsteqn._eval_power(tsteqn) == Equation(a**a, (b/c)**(b/c))
    assert tsteqn._eval_power(a) == Equation(a**a, (b/c)**a)


def test_outputs(capsys):
    from algebra_with_sympy import algwsym_config
    from algebra_with_sympy.algebraic_equation import __latex_override__, \
        __command_line_printing__

    # check defaults
    assert algwsym_config.output.show_code == False
    assert algwsym_config.output.human_text == True
    assert algwsym_config.output.label == True
    assert algwsym_config.output.solve_to_list == False

    a, b, c = symbols('a b c')
    tsteqn = Eqn(a, b/c)
    assert tsteqn.__str__() == 'a = b/c'
    assert latex(tsteqn) == 'a=\\frac{b}{c}'
    assert tsteqn.__repr__() == 'Equation(a, b/c)'
    assert tsteqn.__repr__() == 'Equation(a, b/c)'
    assert tsteqn.__str__() == 'a = b/c'
    assert latex(tsteqn) == 'a=\\frac{b}{c}'

    import __main__ as gs
    vars(gs)['tsteqn'] = tsteqn
    assert tsteqn._get_eqn_name() == 'tsteqn'
    __command_line_printing__(tsteqn)
    captured = capsys.readouterr()
    assert captured.out == 'a = b/c          (tsteqn)\n'
    # make sure sys.displayhook does not point to __command_line_printing__()
    import sys
    sys.displayhook = sys.__displayhook__
    assert __latex_override__(tsteqn) == ('$a=\\frac{b}{c}\\,\\,\\,\\,\\,\\,'
                                          '\\,\\,\\,\\,$(tsteqn)')
    algwsym_config.output.label = False
    __command_line_printing__(tsteqn)
    captured = capsys.readouterr()
    assert captured.out == 'a = b/c\n'
    assert __latex_override__(tsteqn) == '$a=\\frac{b}{c}$'
    algwsym_config.output.label = True

    f = Function("f")(a, b, c)
    eq = Eqn(f, 2)
    assert latex(eq) == "f{\\left(a,b,c \\right)}=2"
    # use custom printer
    assert my_latex(eq) == "f=2"

    x, y = symbols('x y', real=True)
    eq1 = Eqn(abs(2*x + y),3)
    eq2 = Eqn(abs(x + 2*y),3)
    B = solve([eq1,eq2],x,y)
    assert B.__repr__() == 'FiniteSet(FiniteSet(Equation(' \
                                              'x, -3), ' \
                                   'Equation(y, 3)), FiniteSet(Equation(x, ' \
                                              '-1), ' \
                                   'Equation(y, -1)), FiniteSet(Equation(x, ' \
                                              '1), ' \
                                   'Equation(y, 1)), FiniteSet(Equation(x, 3),' \
                                   ' Equation(y, -3)))'
    assert B.__str__() == '{{x = -3, y = 3}, {x = -1, y = -1}, ' \
                                   '{x = 1, y = 1}, {x = 3, y = -3}}'
    __command_line_printing__(B)
    captured = capsys.readouterr()
    assert captured.out == \
           '{{x = -3, y = 3}, {x = -1, y = -1}, ' \
                                   '{x = 1, y = 1}, {x = 3, y = -3}}\n'

    algwsym_config.output.show_code = True
    __command_line_printing__(B)
    captured = capsys.readouterr()
    assert captured.out== \
           'Code version: FiniteSet(FiniteSet(' \
        'Equation(x, -3), Equation(y, 3)), FiniteSet(Equation(x, -1), ' \
        'Equation(y, -1)), FiniteSet(Equation(x, 1), Equation(y, 1)), ' \
        'FiniteSet(Equation(x, 3), Equation(y, -3)))' \
    '\n{{x = -3, y = 3}, {x = -1, y = -1}, {x = 1, y = 1}, {x = 3, y = -3}}\n'
    assert __latex_override__(B) == \
    '$\\left\\{\\left\\{x=-3, y=3\\right\\}, \\left\\{x=-1, ' \
           'y=-1\\right\\}, \\left\\{x=1, y=1\\right\\}, ' \
            '\\left\\{x=3, y=-3\\right\\}\\right\\}$'
    captured = capsys.readouterr()
    assert captured.out == \
           'Code version: FiniteSet(FiniteSet(' \
           'Equation(x, -3), Equation(y, 3)), FiniteSet(Equation(x, -1), ' \
           'Equation(y, -1)), FiniteSet(Equation(x, 1), Equation(y, 1)), ' \
           'FiniteSet(Equation(x, 3), Equation(y, -3)))\n'

    algwsym_config.output.show_code = False
    algwsym_config.output.human_text = False
    __command_line_printing__(B)
    captured = capsys.readouterr()
    assert captured.out == 'FiniteSet(FiniteSet(Equation(x, -3), ' \
                            'Equation(y, 3)), FiniteSet(Equation(x, -1), ' \
                            'Equation(y, -1)), FiniteSet(Equation(x, 1), ' \
                            'Equation(y, 1)), FiniteSet(Equation(x, 3), ' \
                            'Equation(y, -3)))\n'

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
    assert root(Eqn(a,b/c),3) == Equation(a**(S(1)/S(3)), (b/c)**(S(1)/S(3)))
    assert root(b/c,3) == (b/c)**(S(1)/S(3))
    assert sqrt(Eqn(a,b/c)) == Equation(sqrt(a), sqrt(b/c))

def test_units():
    units('J mol K')
    user_namespace = None
    import sys
    frame_num = 0
    frame_name = None
    while frame_name != '__main__' and frame_num < 50:
        user_namespace = sys._getframe(frame_num).f_globals
        frame_num += 1
        frame_name = user_namespace['__name__']
    J = user_namespace['J']
    mol = user_namespace['mol']
    K = user_namespace['K']
    assert sqrt((123.2*J/mol/K)**2) == 123.2*J/mol/K
    assert 1.0*J + 5.0*J == 6.0*J
    assert 1.0*J + 5.0*mol == 1.0*J + 5.0*mol
    assert J > 0 and mol > 0 and K > 0

def test_solve():
    a, b, c, x = symbols('a b c x')
    assert Equation(x, ((b - sqrt(4*a*c + b**2))/(2*a)).expand()) in solve(
        Equation(a*x**2,b*x+c),x)
    assert Equation(x, ((b + sqrt(4*a*c + b**2))/(2*a)).expand()) in solve(
        Equation(a*x**2,b*x+c),x)
    assert len(solve(Equation(a*x**2,b*x+c), x)) == 2
    result = solve(a*x**2-b*x-c,x)
    solns = []
    for k in result:
        for key in k.keys():
            solns.append(k[key])
    assert ((b - sqrt(4*a*c + b**2))/(2*a)).expand() in solns

    x, y = symbols('x y', real = True)
    eq1 = Eqn(abs(2*x + y), 3)
    eq2 = Eqn(abs(x + 2*y), 3)
    assert solve([eq1,eq2], x, y) == FiniteSet(FiniteSet(Equation(x, -3),
                                   Equation(y, 3)), FiniteSet(Equation(x, -1),
                                   Equation(y, -1)), FiniteSet(Equation(x, 1),
                                   Equation(y, 1)), FiniteSet(Equation(x, 3),
                                   Equation(y, -3)))
    algwsym_config.output.solve_to_list = True
    assert solve([eq1,eq2], x, y) == [[Equation(x, -3), Equation(y, 3)],
                                      [Equation(x, -1), Equation(y, -1)],
                                      [Equation(x, 1), Equation(y, 1)],
                                      [Equation(x, 3), Equation(y, -3)]]
    
    xi, wn = symbols("xi omega_n", real=True, positive=True)
    Tp, Ts = symbols("T_p, T_s", real=True, positive=True)
    e1 = Eqn(Tp, pi / (wn*sqrt(1 - xi**2)))
    e2 = Eqn(Ts, 4 / (wn*xi))
    algwsym_config.output.solve_to_list = False
    assert solve([e1, e2], [xi, wn]) == FiniteSet(
        Eqn(xi, 4*Tp/sqrt(16*Tp**2 + pi**2*Ts**2)),
        Eqn(wn, sqrt(16*Tp**2 + pi**2*Ts**2)/(Tp*Ts)))
    algwsym_config.output.solve_to_list = True
    assert solve([e1, e2], [xi, wn]) == [
        Eqn(xi, 4*Tp/sqrt(16*Tp**2 + pi**2*Ts**2)),
        Eqn(wn, sqrt(16*Tp**2 + pi**2*Ts**2)/(Tp*Ts))
    ]
    # order of symbols are swapped -> results are swapped as well
    assert solve([e1, e2], [wn, xi]) == [
        Eqn(wn, sqrt(16*Tp**2 + pi**2*Ts**2)/(Tp*Ts)),
        Eqn(xi, 4*Tp/sqrt(16*Tp**2 + pi**2*Ts**2))
    ]

def test_Heaviside():
    a, b, c, x = symbols('a b c x')
    tsteqn = Equation(a, b / c)
    assert (Heaviside(tsteqn) ==
            Equation(Heaviside(tsteqn.lhs), Heaviside(tsteqn.rhs)))
    assert Heaviside(0) == S(1)/S(2)

def test_equality_extension():
    a, b, c, x = symbols('a b c x')
    tstequal = Equality(a, b / c)
    assert(tstequal.to_Equation() == Equation(a, b / c))
    assert(tstequal.to_Eqn()== Equation(a, b / c))

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


def test_rewrite_add():
    b, x = symbols("x, b")
    eq = Equation(x + b, x - b)
    assert eq.rewrite(Add) == Equation(2 * b, 0)
    assert set(eq.rewrite(Add, evaluate=None).lhs.args) == set((b, x, b, -x))
    assert set(eq.rewrite(Add, evaluate=False).lhs.args) == set((b, x, b, -x))
    assert eq.rewrite(Add, eqn=False) == 2 * b
    assert set(eq.rewrite(Add, eqn=False, evaluate=False).args) == set((b, x, b, -x))


def test_rewrite():
    x = symbols("x")
    eq = Equation(exp(I*x),cos(x) + I*sin(x))

    # NOTE: Must use `sexp` otherwise the test is going to fail.
    # This reflects the fact that rewrite pulls the fuction exp internally
    # from the definitions of functions in sympy and not from the globally
    # redefined functions that are Equation aware.
    from sympy import exp as sexp
    assert eq.rewrite(exp) == Equation(exp(I*x), sexp(I*x))
    assert eq.rewrite(Add) == Equation(exp(I*x) - I*sin(x) - cos(x), 0)


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

    # verify the effectiveness of `simultaneous`
    eq = Equation((x + a) / a, b * c)
    sd = {x + a: a, a: x + a}
    assert eq.subs(sd) == Equation(1, b * c)
    assert eq.subs(sd, simultaneous=True) == Equation(a / (x + a), b * c)

def test_issue_23():
    # This gave a key error
    a, t = symbols('a t')
    assert simplify(a * cos(t) + sin(t)) == a * cos(t) + sin(t)
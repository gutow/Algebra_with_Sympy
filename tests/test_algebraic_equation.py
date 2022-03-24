from sympy import symbols, integrate, simplify, expand, factor, log, Integral, \
    diff, FiniteSet, Equality, Function, functions, Matrix, S
from .algebraic_equation import solve, collect, Equation, Eqn, sqrt, root
from .algebraic_equation import algwsym_config

from pytest import raises

#####
# Extension of the Function class. For incorporation into SymPy this should
# become part of the class
#####
class Function(Function):
    def __new__(cls, *args, **kwargs):
        n = len(args)
        eqnloc = None
        neqns = 0
        newargs = []
        for k in args:
            newargs.append(k)
        if (n > 0):
            for i in range(n):
                if isinstance(args[i], Equation):
                    neqns += 1
                    eqnloc = i
            if neqns > 1:
                raise NotImplementedError('Function calls with more than one '
                                          'Equation as a parameter are not '
                                          'supported. You may be able to get '
                                          'your desired outcome using .applyrhs'
                                          ' and .applylhs.')
            if neqns == 1:
                newargs[eqnloc] = args[eqnloc].lhs
                lhs = super().__new__(cls, *newargs, **kwargs)
                newargs[eqnloc] = args[eqnloc].rhs
                rhs = super().__new__(cls, *newargs, **kwargs)
                return Equation(lhs,rhs)
        return super().__new__(cls, *args, **kwargs)

for func in functions.__all__:
    # TODO: This will not be needed when incorporated into SymPy listed in
    #  `skip` cannot be extended because of `mro` error or `metaclass
    #  conflict`. Seems to reflect expectation that a helper function will be
    #  defined within the object (e.g. `_eval_power()` for all the flavors of
    #  `root`).
    skip = ('sqrt', 'root', 'Min', 'Max', 'Id', 'real_root', 'cbrt',
            'unbranched_argument', 'polarify', 'unpolarify',
            'piecewise_fold', 'E1', 'Eijk', 'bspline_basis',
            'bspline_basis_set', 'interpolating_spline', 'jn_zeros',
            'jacobi_normalized', 'Ynm_c')
    if func not in skip:
        execstr = 'from sympy import ' + str(func)
        exec(execstr, globals(), locals())
        execstr = 'class ' + str(func) + '(' + str(
            func) + ',Function):\n    pass\n'
        exec(execstr, globals(), locals())

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
    assert tsteqn._latex(tsteqn) == 'a=\\frac{b}{c}'

def test_sympy_functions():
    # TODO: To avoid problems if a function in sympy changes or is added this
    #  should test all functions automatically.
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
    assert Equation(x, (b - sqrt(4*a*c + b**2))/(2*a)) in solve(Equation(
        a*x**2,b*x+c),x)
    assert Equation(x, (b + sqrt(4*a*c + b**2))/(2*a)) in solve(Equation(
        a*x**2,b*x+c),x)
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

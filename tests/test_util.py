from sympy import symbols, Equation, Eqn, oo
from algebra_with_sympy.util import (_get_user_ns, __get_algwsym_config,
                                     __get_sympy_expr_name__, _isnumber)
from algebra_with_sympy.algebraic_equation import Config

###
# The routines tested here look for values that will be in the __main__
# namespace during an interactive run. As the Algebra_with_Sympy tools are
# meant to run interactively this is what is being tested.
###

def test_get_user_ns():
    ns = _get_user_ns()
    if ns:
        setattr(ns,'algwsym_config',Config())
        assert (hasattr(ns,'algwsym_config'))
    # cleanup
    delattr(ns, 'algwsym_config')

def test__get_algwsym_config():
    # If `test_get_user_ns()` passes then this can run as there is a __main__
    # to test things against.
    ns = _get_user_ns()
    setattr(ns, 'algwsym_config', Config())
    tstconfig = __get_algwsym_config()
    assert(hasattr(tstconfig,'output'))
    assert(hasattr(tstconfig,'numerics'))
    # cleanup
    delattr(ns, 'algwsym_config')

def test__get_sympy_expr_name():
    # This is checking for things in __main__. However, it is not running in
    # __main__. So the objects to search for are defined twice in __main__
    # and then also assigned to a local value.
    a, b, x = symbols('a b x')
    ns = _get_user_ns()
    setattr(ns, 'tstexpr', a/b)
    tstexpr = getattr(ns, 'tstexpr')
    assert(__get_sympy_expr_name__(tstexpr) == 'tstexpr')
    setattr(ns, 'tsteqn', Eqn(x, a/b))
    tsteqn = getattr(ns, 'tsteqn')
    assert (__get_sympy_expr_name__(tsteqn) == 'tsteqn')
    # cleanup
    delattr(ns, 'tstexpr')
    delattr(ns, 'tsteqn')

def test__isnumber():
    a, b, = symbols('a b')
    assert _isnumber(a) == False
    assert _isnumber(b) == False
    assert _isnumber(1.0) == True
    assert _isnumber(1) == True
    assert _isnumber(oo) == False
    b = 2.0
    a = 1
    assert _isnumber(a) == True
    assert _isnumber(b) == True

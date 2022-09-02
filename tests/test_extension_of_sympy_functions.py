from pytest import raises

from algebra_with_sympy.algebraic_equation import str_to_extend_sympy_func
from algebra_with_sympy.algebraic_equation import Equation, EqnFunction
from algebra_with_sympy.algebraic_equation import _extended_, _skip_
from sympy import functions, FunctionClass, symbols
import importlib
temp = importlib.import_module('sympy', package=functions.__all__)
for func in functions.__all__:
    globals()[func] = getattr(temp, func)
temp = importlib.import_module('algebra_with_sympy.algebraic_equation',
                               package=_extended_)
# Needed for some tests so that extended functions are in the correct
# namespace.
for func in _extended_:
    globals()[func] = getattr(temp, func)

for func in functions.__all__:
    if func not in _skip_:
        try:
            # The string that is executed has a test function below.
            exec(str_to_extend_sympy_func(func), globals(), locals())
        except TypeError:
            from warnings import warn
            warn('SymPy function/operation ' + str(func) + ' may not work ' \
                'properly with Equations. If you use it with Equations, ' \
                'validate its behavior. We are working to address this ' \
                'issue.')

def test_sympy_import():
    for func in functions.__all__:
        if func not in _skip_:
            assert(str(func) in globals())
            assert(isinstance(globals()[func],FunctionClass))
    pass

def test_str_to_extend_sympy_func():
    teststr = 'testname'
    execstr = 'class %S(%S,EqnFunction):\n    pass\n'
    execstr = execstr.replace('%S',str(teststr))
    assert str_to_extend_sympy_func(teststr)==execstr
    pass

def test_functions_extensions():
    from inspect import signature
    failures = []
    a, b , c = symbols('a b c')
    eq = Equation(a, b/c)
    n = symbols('n', positive = True, integer = True)
    for func in functions.__all__:
        if func not in _skip_ or func in _extended_:
            obj = globals()[func]
            sig = signature(obj).parameters
            if func == 'betainc' or func == 'betainc_regularized':
                # The signature is undefined need 4 complex numbers:
                # a, b, x1, x2.
                sig = {'arg1':'a','arg2':'b','arg3':'x1','arg4':'x2'}
            keylist = [key for key in sig]
            tempargs = [eq]
            largs = [eq.lhs]
            rargs = [eq.rhs]
            for key in sig:
                if (str(sig[key]).find("="))==-1 and (str(sig[key]).
                        find("**"))==-1 and key != keylist[0]:
                    tempargs.append(n)
                    largs.append(n)
                    rargs.append(n)
            try:
                tst = obj(*tempargs)
                if not (tst == Equation(obj(*largs),obj(*rargs))):
                    failures.append(func + ' extended but did not work.')
            except Exception as e:
                failures.append(str(func) +': '+str(e))
    assert(failures == [])
    pass

def test_functions_extensions_eqn_not_arg1():
    from inspect import signature
    failures = []
    a, b , c = symbols('a b c')
    eq = Equation(a, b/c)
    n = symbols('n', positive = True, integer = True)
    for func in functions.__all__:
        if func not in _skip_ or func in _extended_:
            obj = globals()[func]
            sig = signature(obj).parameters
            if func == 'betainc' or func == 'betainc_regularized':
                # The signature is undefined need 4 complex numbers:
                # a, b, x1, x2.
                sig = {'arg1':'a','arg2':'b','arg3':'x1','arg4':'x2'}
            keylist = [key for key in sig]
            for j in range(1, len(sig)):
                tempargs = [n]
                largs = [n]
                rargs = [n]
                for k in range(1,len(sig)):
                    if ((str(sig[keylist[k]]).find("=")) == -1 and
                        (str(sig[keylist[k]]).find("**")) == -1):
                        if k == j:
                            tempargs.append(eq)
                            largs.append(eq.lhs)
                            rargs.append(eq.rhs)
                        else:
                            tempargs.append(n)
                            largs.append(n)
                            rargs.append(n)
                try:
                    tst = obj(*tempargs)
                    if (isinstance(tst, Equation) and not
                    (tst == Equation(obj(*largs), obj(*rargs)))):
                        failures.append(func + '('+str(*tempargs)+ ') ' \
                                 'extended but did not work.')
                except Exception as e:
                    failures.append(str(func) +': '+str(e))
    assert(failures == [])
    pass

def test_two_eqn():
    a, b, c = symbols('a b c')
    eq = Equation(a, b / c)
    obj = globals()['besselj']
    raises(NotImplementedError, lambda: obj(eq,eq))
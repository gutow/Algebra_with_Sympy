from .algebraic_equation import str_to_extend_sympy_func
from .algebraic_equation import _skip_
from sympy import functions, FunctionClass
import importlib
temp = importlib.import_module('sympy',package=functions.__all__)
for func in functions.__all__:
    globals()[func] = getattr(temp,func)

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

def extend_sympy_func(func):
    try:
        exec(str_to_extend_sympy_func(func), globals(), locals())
    except TypeError:
        from warnings import warn
        warn('SymPy function/operation ' + str(func) + ' may not work ' \
                   'properly with Equations. If you use it with Equations, ' \
                   'validate its behavior. We are working to address this ' \
                   'issue.')
        return str(func)+' failed to extend.'
    return True

"""
def test_functions_extensions():
    failures = []
    a, b , c = symbols('a b c')
    eq = Equation(a, b/c)
    for func in functions.__all__:
        if func not in _skip_:
            result = extend_sympy_func(func)
            if isinstance(result,str):
                failures.append(result)
            obj = globals()[func]
            try:
                tst = obj(eq)
                if not (tst == Equation(obj(a),obj(b/c))):
                    failures.append(func + ' extended but not into same '
                                           'namespace.')
            except Exception as e:
                failures.append(e)
    assert(failures == [])
    pass
"""
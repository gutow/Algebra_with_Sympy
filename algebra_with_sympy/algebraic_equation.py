"""
This package uses a special version of sympy which defines an equation 
with a left-hand-side (lhs) and a right-
hand-side (rhs) connected by the "=" operator (e.g. `p*V = n*R*T`).

The intent is to allow using the mathematical tools in SymPy to rearrange
equations and perform algebra in a stepwise fashion. In this way more people
can successfully perform algebraic rearrangements without stumbling over
missed details such as a negative sign. This mimics the capabilities available
in [SageMath](https://www.sagemath.org/) and
[Maxima](http://maxima.sourceforge.net/).

This package also provides convenient settings for interactive use on the 
command line, in ipython and Jupyter notebook environments. See the 
documentation at https://gutow.github.io/Algebra_with_Sympy/.

Explanation
===========
This class defines relations that all high school and college students
would recognize as mathematical equations. At present only the "=" relation
operator is recognized.

This class is intended to allow using the mathematical tools in SymPy to
rearrange equations and perform algebra in a stepwise fashion. In this
way more people can successfully perform algebraic rearrangements without
stumbling over missed details such as a negative sign.

Create an equation with the call ``Equation(lhs,rhs)``, where ``lhs`` and
``rhs`` are any valid Sympy expression. ``Eqn(...)`` is a synonym for
``Equation(...)``.

Parameters
==========
lhs: sympy expression, ``class Expr``.
rhs: sympy expression, ``class Expr``.
kwargs:

Examples
========
NOTE: All the examples below are in vanilla python. You can get human
readable eqautions "lhs = rhs" in vanilla python by adjusting the settings
in `algwsym_config` (see it's documentation). Output is human readable by
default in IPython and Jupyter environments.
>>> from algebra_with_sympy import *
>>> a, b, c, x = var('a b c x')
>>> Equation(a,b/c)
Equation(a, b/c)
>>> t=Eqn(a,b/c)
>>> t
Equation(a, b/c)
>>> t*c
Equation(a*c, b)
>>> c*t
Equation(a*c, b)
>>> exp(t)
Equation(exp(a), exp(b/c))
>>> exp(log(t))
Equation(a, b/c)

Simplification and Expansion
>>> f = Eqn(x**2 - 1, c)
>>> f
Equation(x**2 - 1, c)
>>> f/(x+1)
Equation((x**2 - 1)/(x + 1), c/(x + 1))
>>> (f/(x+1)).simplify()
Equation(x - 1, c/(x + 1))
>>> simplify(f/(x+1))
Equation(x - 1, c/(x + 1))
>>> (f/(x+1)).expand()
Equation(x**2/(x + 1) - 1/(x + 1), c/(x + 1))
>>> expand(f/(x+1))
Equation(x**2/(x + 1) - 1/(x + 1), c/(x + 1))
>>> factor(f)
Equation((x - 1)*(x + 1), c)
>>> f.factor()
Equation((x - 1)*(x + 1), c)
>>> f2 = f+a*x**2+b*x +c
>>> f2
Equation(a*x**2 + b*x + c + x**2 - 1, a*x**2 + b*x + 2*c)
>>> collect(f2,x)
Equation(b*x + c + x**2*(a + 1) - 1, a*x**2 + b*x + 2*c)

Apply operation to only one side
>>> poly = Eqn(a*x**2 + b*x + c*x**2, a*x**3 + b*x**3 + c*x)
>>> poly.applyrhs(factor,x)
Equation(a*x**2 + b*x + c*x**2, x*(c + x**2*(a + b)))
>>> poly.applylhs(factor)
Equation(x*(a*x + b + c*x), a*x**3 + b*x**3 + c*x)
>>> poly.applylhs(collect,x)
Equation(b*x + x**2*(a + c), a*x**3 + b*x**3 + c*x)

``.apply...`` also works with user defined python functions
>>> def addsquare(eqn):
...     return eqn+eqn**2
...
>>> t.apply(addsquare)
Equation(a**2 + a, b**2/c**2 + b/c)
>>> t.applyrhs(addsquare)
Equation(a, b**2/c**2 + b/c)
>>> t.apply(addsquare, side = 'rhs')
Equation(a, b**2/c**2 + b/c)
>>> t.applylhs(addsquare)
Equation(a**2 + a, b/c)
>>> addsquare(t)
Equation(a**2 + a, b**2/c**2 + b/c)

Inaddition to ``.apply...`` there is also the less general ``.do``,
``.dolhs``, ``.dorhs``, which only works for operations defined on the
``Expr`` class (e.g.``.collect(), .factor(), .expand()``, etc...).
>>> poly.dolhs.collect(x)
Equation(b*x + x**2*(a + c), a*x**3 + b*x**3 + c*x)
>>> poly.dorhs.collect(x)
Equation(a*x**2 + b*x + c*x**2, c*x + x**3*(a + b))
>>> poly.do.collect(x)
Equation(b*x + x**2*(a + c), c*x + x**3*(a + b))
>>> poly.dorhs.factor()
Equation(a*x**2 + b*x + c*x**2, x*(a*x**2 + b*x**2 + c))

``poly.do.exp()`` or other sympy math functions will raise an error.

Rearranging an equation (simple example made complicated as illustration)
>>> p, V, n, R, T = var('p V n R T')
>>> eq1=Eqn(p*V,n*R*T)
>>> eq1
Equation(V*p, R*T*n)
>>> eq2 =eq1/V
>>> eq2
Equation(p, R*T*n/V)
>>> eq3 = eq2/R/T
>>> eq3
Equation(p/(R*T), n/V)
>>> eq4 = eq3*R/p
>>> eq4
Equation(1/T, R*n/(V*p))
>>> 1/eq4
Equation(T, V*p/(R*n))
>>> eq5 = 1/eq4 - T
>>> eq5
Equation(0, -T + V*p/(R*n))

Substitution (#'s and units)
>>> L, atm, mol, K = var('L atm mol K', positive=True, real=True) # units
>>> eq2.subs({R:0.08206*L*atm/mol/K,T:273*K,n:1.00*mol,V:24.0*L})
Equation(p, 0.9334325*atm)
>>> eq2.subs({R:0.08206*L*atm/mol/K,T:273*K,n:1.00*mol,V:24.0*L}).evalf(4)
Equation(p, 0.9334*atm)

Substituting an equation into another equation:
>>> P, P1, P2, A1, A2, E1, E2 = symbols("P, P1, P2, A1, A2, E1, E2")
>>> eq1 = Eqn(P, P1 + P2)
>>> eq2 = Eqn(P1 / (A1 * E1), P2 / (A2 * E2))
>>> P1_val = (eq1 - P2).swap
>>> P1_val
Equation(P1, P - P2)
>>> eq2 = eq2.subs(P1_val)
>>> eq2
Equation((P - P2)/(A1*E1), P2/(A2*E2))
>>> P2_val = solve(eq2.subs(P1_val), P2).args[0]
>>> P2_val
Equation(P2, A2*E2*P/(A1*E1 + A2*E2))

Combining equations (Math with equations: lhs with lhs and rhs with rhs)
>>> q = Eqn(a*c, b/c**2)
>>> q
Equation(a*c, b/c**2)
>>> t
Equation(a, b/c)
>>> q+t
Equation(a*c + a, b/c + b/c**2)
>>> q/t
Equation(c, 1/c)
>>> t**q
Equation(a**(a*c), (b/c)**(b/c**2))

Utility operations
>>> t.reversed
Equation(b/c, a)
>>> t.swap
Equation(b/c, a)
>>> t.lhs
a
>>> t.rhs
b/c
>>> t.as_Boolean()
Eq(a, b/c)

`.check()` convenience method for `.as_Boolean().simplify()`
>>> from sympy import I, pi
>>> Equation(pi*(I+2), pi*I+2*pi).check()
True
>>> Eqn(a,a+1).check()
False

Differentiation
Differentiation is applied to both sides if the wrt variable appears on
both sides.
>>> q=Eqn(a*c, b/c**2)
>>> q
Equation(a*c, b/c**2)
>>> diff(q,b)
Equation(Derivative(a*c, b), c**(-2))
>>> diff(q,c)
Equation(a, -2*b/c**3)
>>> diff(log(q),b)
Equation(Derivative(log(a*c), b), 1/b)
>>> diff(q,c,2)
Equation(Derivative(a, c), 6*b/c**4)

If you specify multiple differentiation all at once the assumption
is order of differentiation matters and the lhs will not be
evaluated.
>>> diff(q,c,b)
Equation(Derivative(a*c, b, c), -2/c**3)

To overcome this specify the order of operations.
>>> diff(diff(q,c),b)
Equation(Derivative(a, b), -2/c**3)

But the reverse order returns an unevaulated lhs (a may depend on b).
>>> diff(diff(q,b),c)
Equation(Derivative(a*c, b, c), -2/c**3)

Integration can only be performed on one side at a time.
>>> q=Eqn(a*c,b/c)
>>> integrate(q,b,side='rhs')
b**2/(2*c)
>>> integrate(q,b,side='lhs')
a*b*c

Make a pretty statement of integration from an equation
>>> Eqn(Integral(q.lhs,b),integrate(q,b,side='rhs'))
Equation(Integral(a*c, b), b**2/(2*c))

Integration of each side with respect to different variables
>>> q.dorhs.integrate(b).dolhs.integrate(a)
Equation(a**2*c/2, b**2/(2*c))

Automatic solutions using sympy solvers. THIS IS EXPERIMENTAL. Please
report issues at https://github.com/gutow/Algebra_with_Sympy/issues.
>>> tosolv = Eqn(a - b, c/a)
>>> solve(tosolv,a)
FiniteSet(Equation(a, b/2 - sqrt(b**2 + 4*c)/2), Equation(a, b/2 + sqrt(b**2 + 4*c)/2))
>>> solve(tosolv, b)
FiniteSet(Equation(b, (a**2 - c)/a))
>>> solve(tosolv, c)
FiniteSet(Equation(c, a**2 - a*b))
"""
import sys

import sympy
from algebra_with_sympy.preparser import integers_as_exact
from sympy import *

class algwsym_config():

    def __init__(self):
        """
        This is a class to hold parameters that control behavior of
        the algebra_with_sympy package.

        Settings
        ========
        Printing
        --------
        In interactive environments the default output of an equation is a
        human readable string with the two sides connected by an equals
        sign or a typeset equation with the two sides connected by an equals sign.
        `print(Eqn)` or `str(Eqn)` will return this human readable text version of
        the equation as well. This is consistent with python standards, but not
        sympy, where `str()` is supposed to return something that can be
        copy-pasted into code. If the equation has a declared name as in `eq1 =
        Eqn(a,b/c)` the name will be displayed to the right of the equation in
        parentheses (eg. `a = b/c    (eq1)`). Use `print(repr(Eqn))` instead of
        `print(Eqn)` or `repr(Eqn)` instead of `str(Eqn)` to get a code
        compatible version of the equation.

        You can adjust this behavior using some flags that impact output:
        * `algwsym_config.output.show_code` default is `False`.
        * `algwsym_config.output.human_text` default is `True`.
        * `algwsym_config.output.label` default is `True`.
        * `algwsym_config.output.latex_as_equations` default is `False`

        In interactive environments you can get both types of output by setting
        the `algwsym_config.output.show_code` flag. If this flag is true
        calls to `latex` and `str` will also print an additional line "code
        version: `repr(Eqn)`". Thus in Jupyter you will get a line of typeset
        mathematics output preceded by the code version that can be copy-pasted.
        Default is `False`.

        A second flag `algwsym_config.output.human_text` is useful in
        text-based interactive environments such as command line python or
        ipython. If this flag is true `repr` will return `str`. Thus the human
        readable text will be printed as the output of a line that is an
        expression containing an equation.
        Default is `True`.

        Setting both of these flags to true in a command line or ipython
        environment will show both the code version and the human readable text.
        These flags impact the behavior of the `print(Eqn)` statement.

        The third flag `algwsym_config.output.label` has a default value of
        `True`. Setting this to `False` suppresses the labeling of an equation
        with its python name off to the right of the equation.

        The fourth flag `algwsym_config.output.latex_as_equations` has
        a default value of `False`. Setting this to `True` wraps
        output as LaTex equations wrapping them in `\\begin{equation}...\\end{
        equation}`.
        """
        pass

    class output():

        def __init__(self):
            """This holds settings that impact output.
            """
            pass

        @property
        def show_code(self):
            """
            If `True` code versions of the equation expression will be
            output in interactive environments. Default = `False`.
            """
            return self.show_code

        @property
        def human_text(self):
            """
            If `True` the human readable equation expression will be
            output in text interactive environments. Default = `False`.
            """
            return self.human_text

        @property
        def solve_to_list(self):
            """
            If `True` the results of a call to `solve(...)` will return a
            Python `list` rather than a Sympy `FiniteSet`. This recovers
            behavior for versions before 0.11.0.

            Note: setting this `True` means that expressions within the
            returned solutions will not be pretty-printed in Jupyter and
            IPython.
            """
            return self.solve_to_list

        @property
        def latex_as_equations(self):
            """
            If `True` any output that is returned as LaTex for
            pretty-printing will be wrapped in the formal Latex for an
            equation. For example rather than
            ```
            $\\frac{a}{b}=c$
            ```
            the output will be
            ```
            \\begin{equation}\\frac{a}{b}=c\\end{equation}
            ```
            """
            return self.latex_as_equation

    class numerics():

        def __init__(self):
            """This class holds settings for how numerical computation and
            inputs are handled.
            """
            pass

        def integers_as_exact(self):
            """**This is a flag for informational purposes and interface
            consistency. Changing the value will not change the behavior.**

            To change the behavior call:
            * `unset_integers_as_exact()` to turn this feature off.
            * `set_integers_as_exact()` to turn this feature on (on by
            default).

            If set to `True` (the default) and if running in an
            IPython/Jupyter environment any number input without a decimal
            will be interpreted as a sympy integer. Thus, fractions and
            related expressions will not evalute to floating point numbers,
            but be maintained as exact expressions (e.g. 2/3 -> 2/3 not the
            float 0.6666...).
            """
            return self.integers_as_exact

def __latex_override__(expr, *arg):
    algwsym_config = False
    ip = False
    try:
        from IPython import get_ipython
        if get_ipython():
            ip = True
    except ModuleNotFoundError:
        pass
    colab = False
    try:
        from google.colab import output
        colab = True
    except ModuleNotFoundError:
        pass
    show_code = False
    latex_as_equations = False
    if ip:
        algwsym_config = get_ipython().user_ns.get("algwsym_config", False)
    else:
        algwsym_config = globals()['algwsym_config']
    if algwsym_config:
        show_code = algwsym_config.output.show_code
        latex_as_equations = algwsym_config.output.latex_as_equations
    if show_code:
        print("Code version: " + repr(expr))
    if latex_as_equations:
        return r'\begin{equation}'+latex(expr)+'\end{equation}'
    else:
        tempstr = ''
        namestr = ''
        if isinstance(expr, Equation):
            namestr = expr._get_eqn_name()
        if namestr != '' and algwsym_config and algwsym_config.output.label:
            tempstr += r'$'+latex(expr)
            # work around for colab's inconsistent handling of mixed latex and
            # plain strings.
            if colab:
                colabname = namestr.replace('_', '\_')
                tempstr += r'\,\,\,\,\,\,\,\,\,\,(' + colabname + ')$'
            else:
                tempstr += r'\,\,\,\,\,\,\,\,\,\,$(' + namestr + ')'
            return tempstr
        else:
            return '$'+latex(expr) + '$'

def __command_line_printing__(expr, *arg):
    # print('Entering __command_line_printing__')
    human_text = True
    show_code = False
    if algwsym_config:
        human_text = algwsym_config.output.human_text
        show_code = algwsym_config.output.show_code
    tempstr = ''
    if show_code:
        tempstr += "Code version: " + repr(expr) + '\n'
    if not human_text:
        return print(tempstr + repr(expr))
    else:
        labelstr = ''
        namestr = ''
        if isinstance(expr, Equation):
            namestr = expr._get_eqn_name()
        if namestr != '' and algwsym_config.output.label:
            labelstr += '          (' + namestr + ')'
        return print(tempstr + str(expr) + labelstr)

# Now we inject the formatting override(s)
ip = None
try:
    from IPython import get_ipython
    ip = get_ipython()
except ModuleNotFoundError:
    ip = false
formatter = None
if ip:
    # In an environment that can display typeset latex
    formatter = ip.display_formatter
    old = formatter.formatters['text/latex'].for_type(Basic,
                                                      __latex_override__)
    # print("For type Basic overriding latex formatter = " + str(old))

    # For the terminal based IPython
    if "text/latex" not in formatter.active_types:
        old = formatter.formatters['text/plain'].for_type(tuple,
                                                    __command_line_printing__)
        # print("For type tuple overriding plain text formatter = " + str(old))
        for k in sympy.__all__:
            if k in globals() and not "Printer" in k:
                if isinstance(globals()[k], type):
                    old = formatter.formatters['text/plain'].\
                        for_type(globals()[k], __command_line_printing__)
                    # print("For type "+str(k)+
                    # " overriding plain text formatter = " + str(old))
else:
    # command line
    # print("Overriding command line printing of python.")
    sys.displayhook = __command_line_printing__

# Numerics controls
def set_integers_as_exact():
    """This operation uses `sympy.interactive.session.int_to_Integer`, which
    causes any number input without a decimal to be interpreted as a sympy
    integer, to pre-parse input cells. It also sets the flag
    `algwsym_config.numerics.integers_as_exact = True` This is the default
    mode of algebra_with_sympy. To turn this off call
    `unset_integers_as_exact()`.
    """
    ip = False
    try:
        from IPython import get_ipython
        ip = True
    except ModuleNotFoundError:
        ip = False
    if ip:
        if get_ipython():
            get_ipython().input_transformers_post.append(integers_as_exact)
            algwsym_config = get_ipython().user_ns.get("algwsym_config", False)
            if algwsym_config:
                algwsym_config.numerics.integers_as_exact = True
            else:
                raise ValueError("The algwsym_config object does not exist.")
    return

def unset_integers_as_exact():
    """This operation disables forcing of numbers input without
    decimals being interpreted as sympy integers. Numbers input without a
    decimal may be interpreted as floating point if they are part of an
    expression that undergoes python evaluation (e.g. 2/3 -> 0.6666...). It
    also sets the flag `algwsym_config.numerics.integers_as_exact = False`.
    Call `set_integers_as_exact()` to avoid this conversion of rational
    fractions and related expressions to floating point. Algebra_with_sympy
    starts with `set_integers_as_exact()` enabled (
    `algwsym_config.numerics.integers_as_exact = True`).
    """
    ip = False
    try:
        from IPython import get_ipython
        ip = True
    except ModuleNotFoundError:
        ip = False
    if ip:
        if get_ipython():
            pre = get_ipython().input_transformers_post
            # The below looks excessively complicated, but more reliably finds the
            # transformer to remove across varying IPython environments.
            for k in pre:
                if "integers_as_exact" in k.__name__:
                    pre.remove(k)
            algwsym_config = get_ipython().user_ns.get("algwsym_config", False)
            if algwsym_config:
                algwsym_config.numerics.integers_as_exact = False
            else:
                raise ValueError("The algwsym_config object does not exist.")

    return

Eqn = Equation
if ip and "text/latex" not in formatter.active_types:
    old = formatter.formatters['text/plain'].for_type(Eqn,
                                                __command_line_printing__)
    # print("For type Equation overriding plain text formatter = " + str(old))

def units(names):
    """
    This operation declares the symbols to be positive values, so that sympy
    will handle them properly when simplifying expressions containing units.
    Units defined this way are just unit symbols. If you want units that are
    aware of conversions see sympy.physics.units.


    :param string names: a string containing a space separated list of
    symbols to be treated as units.

    :return string list of defined units: calls `name = symbols(name,
    positive=True)` in the interactive namespace for each symbol name.
    """
    from sympy.core.symbol import symbols
    #import __main__ as shell
    user_namespace = None
    try:
        from IPython import get_ipython
        if get_ipython():
            user_namespace = get_ipython().user_ns
    except ModuleNotFoundError:
        pass
    syms = names.split(' ')
    retstr = ''

    if user_namespace==None:
        import sys
        frame_num = 0
        frame_name = None
        while frame_name != '__main__' and frame_num < 50:
            user_namespace = sys._getframe(frame_num).f_globals
            frame_num +=1
            frame_name = user_namespace['__name__']
    retstr +='('
    for k in syms:
        user_namespace[k] = symbols(k, positive = True)
        retstr += k + ','
    retstr = retstr[:-1] + ')'
    return retstr


def solve(f, *symbols, **flags):
    """
    Override of sympy `solve()`.

    If passed an expression and variable(s) to solve for it behaves
    almost the same as normal solve with `dict = True`, except that solutions
    are wrapped in a FiniteSet() to guarantee that the output will be pretty
    printed in Jupyter like environments.

    If passed an equation or equations it returns solutions as a
    `FiniteSet()` of solutions, where each solution is represented by an
    equation or set of equations.

    To get a Python `list` of solutions (pre-0.11.0 behavior) rather than a
    `FiniteSet` issue the command `algwsym_config.output.solve_to_list = True`.
    This also prevents pretty-printing in IPython and Jupyter.

    Examples
    --------
    >>> a, b, c, x, y = symbols('a b c x y', real = True)
    >>> import sys
    >>> sys.displayhook = __command_line_printing__ # set by default on normal initialization.
    >>> eq1 = Eqn(abs(2*x+y),3)
    >>> eq2 = Eqn(abs(x + 2*y),3)
    >>> B = solve((eq1,eq2))

    Default human readable output on command line
    >>> B
    {{x = -3, y = 3}, {x = -1, y = -1}, {x = 1, y = 1}, {x = 3, y = -3}}

    To get raw output turn off by setting
    >>> algwsym_config.output.human_text=False
    >>> B
    FiniteSet(FiniteSet(Equation(x, -3), Equation(y, 3)), FiniteSet(Equation(x, -1), Equation(y, -1)), FiniteSet(Equation(x, 1), Equation(y, 1)), FiniteSet(Equation(x, 3), Equation(y, -3)))

    Pre-0.11.0 behavior where a python list of solutions is returned
    >>> algwsym_config.output.solve_to_list = True
    >>> solve((eq1,eq2))
    [[Equation(x, -3), Equation(y, 3)], [Equation(x, -1), Equation(y, -1)], [Equation(x, 1), Equation(y, 1)], [Equation(x, 3), Equation(y, -3)]]
    >>> algwsym_config.output.solve_to_list = False # reset to default

    `algwsym_config.output.human_text = True` with
    `algwsym_config.output.how_code=True` shows both.
    In Jupyter-like environments `show_code=True` yields the Raw output and
    a typeset version. If `show_code=False` (the default) only the
    typeset version is shown in Jupyter.
    >>> algwsym_config.output.show_code=True
    >>> algwsym_config.output.human_text=True
    >>> B
    Code version: FiniteSet(FiniteSet(Equation(x, -3), Equation(y, 3)), FiniteSet(Equation(x, -1), Equation(y, -1)), FiniteSet(Equation(x, 1), Equation(y, 1)), FiniteSet(Equation(x, 3), Equation(y, -3)))
    {{x = -3, y = 3}, {x = -1, y = -1}, {x = 1, y = 1}, {x = 3, y = -3}}
    """
    from sympy.solvers.solvers import solve
    from sympy.sets.sets import FiniteSet
    newf =[]
    solns = []
    displaysolns = []
    contains_eqn = False
    if hasattr(f,'__iter__'):
        for k in f:
            if isinstance(k, Equation):
                newf.append(k.lhs-k.rhs)
                contains_eqn = True
            else:
                newf.append(k)
    else:
        if isinstance(f, Equation):
            newf.append(f.lhs - f.rhs)
            contains_eqn = True
        else:
            newf.append(f)
    flags['dict'] = True
    result = solve(newf, *symbols, **flags)
    if len(symbols) == 1 and hasattr(symbols[0], "__iter__"):
        symbols = symbols[0]
    if contains_eqn:
        if len(result[0]) == 1:
            for k in result:
                for key in k.keys():
                    val = k[key]
                    tempeqn = Eqn(key, val)
                    solns.append(tempeqn)
            if len(solns) == len(symbols):
                # sort according to the user-provided symbols
                solns = sorted(solns, key=lambda x: symbols.index(x.lhs))
        else:
            for k in result:
                solnset = []
                for key in k.keys():
                    val = k[key]
                    tempeqn = Eqn(key, val)
                    solnset.append(tempeqn)
                if not algwsym_config.output.solve_to_list:
                    solnset = FiniteSet(*solnset)
                else:
                    if len(solnset) == len(symbols):
                        # sort according to the user-provided symbols
                        solnset = sorted(solnset, key=lambda x: symbols.index(x.lhs))
                solns.append(solnset)
    else:
        solns = result
    if algwsym_config.output.solve_to_list:
        if len(solns) == 1 and hasattr(solns[0], "__iter__"):
            # no need to wrap a list of a single element inside another list
            return solns[0]
        return solns
    else:
        if len(solns) == 1:
            # do not wrap a singleton in FiniteSet if it already is
            for k in solns:
                if isinstance(k, FiniteSet):
                    return k
        return FiniteSet(*solns)

def solveset(f, symbols, domain=sympy.Complexes):
    """
    Very experimental override of sympy solveset, which we hope will replace
    solve. Much is not working. It is not clear how to input a system of
    equations unless you directly select `linsolve`, etc...
    """
    from sympy.solvers import solveset as solve
    newf = []
    solns = []
    displaysolns = []
    contains_eqn = False
    if hasattr(f, '__iter__'):
        for k in f:
            if isinstance(k, Equation):
                newf.append(k.lhs - k.rhs)
                contains_eqn = True
            else:
                newf.append(k)
    else:
        if isinstance(f, Equation):
            newf.append(f.lhs - f.rhs)
            contains_eqn = True
        else:
            newf.append(f)
    result = solve(*newf, symbols, domain=domain)
    # if contains_eqn:
    #     if len(result[0]) == 1:
    #         for k in result:
    #             for key in k.keys():
    #                 val = k[key]
    #                 tempeqn = Eqn(key, val)
    #                 solns.append(tempeqn)
    #         display(*solns)
    #     else:
    #         for k in result:
    #             solnset = []
    #             displayset = []
    #             for key in k.keys():
    #                 val = k[key]
    #                 tempeqn = Eqn(key, val)
    #                 solnset.append(tempeqn)
    #                 if algwsym_config.output.show_solve_output:
    #                     displayset.append(tempeqn)
    #             if algwsym_config.output.show_solve_output:
    #                 displayset.append('-----')
    #             solns.append(solnset)
    #             if algwsym_config.output.show_solve_output:
    #                 for k in displayset:
    #                     displaysolns.append(k)
    #         if algwsym_config.output.show_solve_output:
    #             display(*displaysolns)
    # else:
    solns = result
    return solns


class Equality(Equality):
    """
    Extension of Equality class to include the ability to convert it to an
    Equation.
    """
    def to_Equation(self):
        """
        Return: recasts the Equality as an Equation.
        """
        return Equation(self.lhs,self.rhs)

    def to_Eqn(self):
        """
        Synonym for to_Equation.
        Return: recasts the Equality as an Equation.
        """
        return self.to_Equation()

Eq = Equality

def __FiniteSet__repr__override__(self):
    """Override of the `FiniteSet.__repr__(self)` to overcome sympy's
    inconsistent wrapping of Finite Sets which prevents reliable use of
    copy and paste of the code representation.
    """
    insidestr = ""
    for k in self.args:
        insidestr += k.__repr__() +', '
    insidestr = insidestr[:-2]
    reprstr = "FiniteSet("+ insidestr + ")"
    return reprstr

sympy.sets.FiniteSet.__repr__ = __FiniteSet__repr__override__

def __FiniteSet__str__override__(self):
    """Override of the `FiniteSet.__str__(self)` to overcome sympy's
    inconsistent wrapping of Finite Sets which prevents reliable use of
    copy and paste of the code representation.
    """
    insidestr = ""
    for k in self.args:
        insidestr += str(k) + ', '
    insidestr = insidestr[:-2]
    strrep = "{"+ insidestr + "}"
    return strrep

sympy.sets.FiniteSet.__str__ = __FiniteSet__str__override__

# Redirect python abs() to Abs()
abs = Abs
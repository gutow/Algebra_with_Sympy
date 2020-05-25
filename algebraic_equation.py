"""
__Algebraic Equations with SymPy__

author: Jonathan Gutow <gutow@uwosh.edu>
date: May 2020
license: GPL V3+

These tools define relations that all high school and college students would recognize as mathematical equations.
They consist of a left hand side (lhs) and a right hand side (rhs) connected by a relation operator such as "=". At
present only the "=" relation operator is recognized.

This tool applies operations to both sides of the equation simultaneously, just as students are taught to do when 
attempting to isolate (solve for) a variable. Thus the statement `Equation/b` yields a new equation `Equation.lhs/b = Equation.rhs/b`

The intent is to allow using the mathematical tools in SymPy to rearrange equations and perform algebra
in a stepwise fashion. In this way more people can successfully perform algebraic rearrangements without stumbling
over missed details such as a negative sign. This mimics the capabilities available in [SageMath]
(https://www.sagemath.org/) and [Maxima](http://maxima.sourceforge.net/), but can be installed in a generic python
environment.
_Setup/Installation_: Currently this tool is not available as a pip installable package. The file `algebraic_equation.py`
must be available for import in the directory space of the active Python, IPython or Jupyter notebook. To activate issue
the command: `from algebraic_equation import *`. This will also import the SymPy tools. If you want to isolate this tool
from the global namespace you are working with change the import statement to `import algebraic_equation as spa`, where 
`spa` stands for "SymPy Algebra". Then all calls would be made to `spa.funcname()`.

Usage examples can be found in the docstrings and the demonstration Jupyter notebook `Demonstration of algebraic_equation.py.ipynb`.
"""
from sympy import *

class Equation(Expr):
    '''
    This class defines relations that all high school and college students would recognize as mathematical equations.
    They consist of a left hand side (lhs) and a right hand side (rhs) connected by a relation operator such as "=". At
    present only the "=" relation operator is recognized.
    
    This class is intended to allow using the mathematical tools in SymPy to rearrange equations and perform algebra
    in a stepwise fashion. In this way more people can successfully perform algebraic rearrangements without stumbling
    over missed details such as a negative sign.
    
    __Note__ that this module imports Sympy into its namespace so there is no need to import Sympy separately.
    
    Create an equation with the call `Equation(lhs,rhs,relation_operator)`, where `lhs` and `rhs` are any valid Sympy
    expression. `relation_operator` defaults to the string "=" if not supplied. Currently,"=" is the only valid option.
    `equ(...)` is a synonym for `Equation(...)`.
    
    Examples:
    >>> var('a b c')
    >>> equ(a,b/c)
        a=b/c
    >>> t=equ(a,b/c)
    >>> t
        a=b/c
    >>> t*c
        a*c=b
    >>> c*t
        a*c=b
    >>> exp(t)
        exp(a)=exp(b/c)
    >>> exp(log(t))
        a=b/c
    '''
    _op_priority = 11.0 # This makes sure the rules for equations are applied before those for expressions
                        # which have _op_priority = 10.0
    
    def __init__(self,lhs,rhs,relop='='):
        if not(relop == '='):
           raise NotImplementedError('"=" is the only relational operator presently supported in Equations.')        
        self.lhs = lhs
        self.rhs = rhs
    
#####
# Overrides of SymPy.Expr Arithmatic
#####
    def __pos__(self):
        return self

    def __neg__(self):
        # Mul has its own __neg__ routine, so we just
        # create a 2-args Mul with the -1 in the canonical
        # slot 0.
        c = self.is_commutative
        lhs =Mul._from_args((S.NegativeOne, self.lhs), c)
        rhs =Mul._from_args((S.NegativeOne, self.rhs), c)        
        return equ(lhs,rhs)

    def __abs__(self):
        from sympy import Abs
        lhs=Abs(self.lhs)
        rhs=Abs(self.rhs)
        return equ(lhs,rhs)

    def __add__(self, other):
        lhs = Add(self.lhs,other)
        rhs = Add(self.rhs,other)
        return equ(lhs,rhs)

    def __radd__(self, other):
        lhs = Add(other,self.lhs)
        rhs = Add(other,self.rhs)
        return equ(lhs,rhs)

    def __sub__(self, other):
        lhs = Add(self.lhs,-other)
        rhs = Add(self.rhs,-other)
        return equ(lhs,rhs)

    def __rsub__(self, other):
        lhs = Add(other,-self.lhs)
        rhs = Add(other,-self.rhs)
        return equ(lhs,rhs)

    def __mul__(self, other):
        lhs = Mul(self.lhs,other)
        rhs = Mul(self.rhs,other)
        return equ(lhs,rhs)
    
    def __rmul__(self, other):
        lhs = Mul(other,self.lhs)
        rhs = Mul(other,self.rhs)
        return equ(lhs,rhs)

    def _pow(self, other):
        lhs = Pow(self.lhs,other)
        rhs = Pow(self.rhs,other)
        return equ(lhs,rhs)

    def __rpow__(self, other):
        lhs = Pow(other,self.lhs)
        rhs = Pow(other,self.rhs)
        return equ(lhs,rhs)

    def __div__(self, other):
        return self.__mul__(Pow(other, S.NegativeOne))

    def __rdiv__(self, other):
        raise NotImplementedError('Division by equation not supported.')

    __truediv__ = __div__
    __rtruediv__ = __rdiv__

    def __mod__(self, other):
        lhs = Mod(self.lhs,other)
        rhs = Mod(self.rhs,other)
        return equ(lhs,rhs)

    def __rmod__(self, other):
        raise NotImplementedError('Modulus by equation not supported.')
            
    def __repr__(self):
        return(str(self.lhs)+' = '+str(self.rhs))
    
    def _latex(self,obj,**kwargs):
        return(latex(self.lhs)+'='+latex(self.rhs))

equ = Equation

class Function(Function):
    def __new__(cls, *arg, **kwargs):
        if (type(arg[0]) is Equation):
            temptuple=(arg[0].lhs,)+arg[1:]
            lhs = super().__new__(cls, *temptuple, **kwargs)
            temptuple=(arg[0].rhs,)+arg[1:]
            rhs = super().__new__(cls, *temptuple, **kwargs)
            return (equ(lhs,rhs))
        else:
            return(super().__new__(cls, *arg, **kwargs))
        
for func in functions.__all__:
    # listed in `skip` cannot be extended because of `mro` error or `metaclass conflict`.
    skip=('sqrt','root','Min','Max','Id','real_root','cbrt','unbranched_argument','polarify','unpolarify',
         'piecewise_fold','E1','Eijk','bspline_basis','bspline_basis_set','interpolating_spline','jn_zeros',
          'jacobi_normalized','Ynm_c')
    bare=('sqrt',)
    if func not in skip:
        execstr = 'class '+str(func)+'('+str(func)+',Function):\n    pass\n'
        exec(execstr,globals(),locals())
#####        
# Manual overrides of some bare functions. This is probably automatable with `inspect`.
#####
###
# override of sqrt
###
from sympy import sqrt as spsqrt
execstr='def sqrt(arg, evaluate=None):\n'
execstr+='    """\n'
# Since all we are doing is adding ability to handle Equations we will import the docstring
execstr+='    '+spsqrt.__doc__+'\n'
execstr+='    """\n'
execstr+='    if (type(arg) is Equation):\n'
execstr+='        lhs = spsqrt(arg.lhs,evaluate)\n'
execstr+='        rhs = spsqrt(arg.rhs,evaluate)\n'
execstr+='        return(Equation(lhs,rhs))\n'
execstr+='    else:\n'
execstr+='        return(spsqrt(arg,evaluate))\n'
execstr+='    def __doc__():\n'
execstr+='        return(spsqrt.__doc__())\n'
exec(execstr,globals(),locals())
        
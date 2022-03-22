__Algebraic Equations with SymPy__

author: Jonathan Gutow <gutow@uwosh.edu>

date: March 2022

license: GPL V3+

This tool defines relations that all high school and college students would
recognize as mathematical equations. 
They consist of a left hand side (lhs) and a right hand side (rhs) connected by
the relation operator "=".

This tool applies operations to both sides of the equation simultaneously, just
as students are taught to do when 
attempting to isolate (solve for) a variable. Thus the statement `Equation/b`
yields a new equation `Equation.lhs/b = Equation.rhs/b`

The intent is to allow using the mathematical tools in SymPy to rearrange
equations and perform algebra
in a stepwise fashion using as close to standard mathematical notation as 
possible. In this way more people can successfully perform 
algebraic rearrangements without stumbling
over missed details such as a negative sign. This mimics the capabilities
available in [SageMath](https://www.sagemath.org/) 
and [Maxima](http://maxima.sourceforge.net/), but can be installed in a generic
python environment.

Once the algebra is complete it is possible to substitute numbers with 
units into the solved equation to calculate a numerical solution with 
proper units.

_Setup/Installation_: Use pip to install in your python environment: 
`python pip -U Algebra_with_SymPy` To use in a running python session issue
the following command : `from algebra_with_sympy import *`. 
This will also import the SymPy tools. If you want to isolate this tool
from the global namespace you are working with change the import statement 
to `import algebra_with_sympy as spa`, where 
`spa` stands for "SymPy Algebra". Then all calls would be made to `
spa.funcname()`.

Usage examples can be found in the docstrings and the demonstration Jupyter 
notebook `Demonstration of equation class.ipynb` in this git repository.

Try in binder: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/gutow/Algebra_with_Sympy.git/master)
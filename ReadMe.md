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
over missed details such as a negative sign. This mimics the capabilities available in [SageMath](https://www.sagemath.org/) 
and [Maxima](http://maxima.sourceforge.net/), but can be installed in a generic python environment.

_Setup/Installation_: Currently this tool is not available as a pip installable package. The file `algebraic_equation.py`
must be available for import in the directory space of the active Python, IPython or Jupyter notebook. To activate issue
the command: `from algebraic_equation import *`. This will also import the SymPy tools. If you want to isolate this tool
from the global namespace you are working with change the import statement to `import algebraic_equation as spa`, where 
`spa` stands for "SymPy Algebra". Then all calls would be made to `spa.funcname()`.

Usage examples can be found in the docstrings and the demonstration Jupyter notebook `Demonstration of algebraic_equation.py.ipynb`. 

Try in binder: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/gutow/Algebra_with_Sympy.git/master)
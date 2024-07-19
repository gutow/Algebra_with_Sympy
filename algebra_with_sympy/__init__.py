"""
.. include:: ../ReadMe.md
.. include:: ../Development Notes.md
"""
__docformat__ = "numpy"
from warnings import warn
proper_sympy = True
try:
    from sympy.core.equation import Equation
except ImportError:
    proper_sympy = False
    warn('You need the extended version of Sympy to use Algebra_with_Sympy. '
         'Algebra_with_Sympy will not be loaded. You can use your current '
         'version of Sympy without the Algebra_with_Sympy features using '
         'the command `from sympy import *`. To get the extended version '
         'of sympy:\n'
         '1. uninstall your current version `pip uninstall sympy`.\n'
         '2. install extended sympy `pip install sympy-for-algebra`.\n'
         'NOTE: an update to extended sympy is usually issued soon after '
         'each 1.XX.1 release of standard sympy.')

if proper_sympy:
    from algebra_with_sympy.algebraic_equation import *

    # Set up numerics behaviors
    try:
        from IPython import get_ipython

        if get_ipython():
            get_ipython().input_transformers_post.append(integers_as_exact)
            algwsym_config.numerics.integers_as_exact = True
    except ModuleNotFoundError:
            pass

    from algebra_with_sympy.preparser import *

    # Set the output formatting defaults
    algwsym_config.output.show_code = False
    algwsym_config.output.human_text = True
    algwsym_config.output.label = True
    algwsym_config.output.solve_to_list = False
    algwsym_config.output.latex_as_equations = False

    # Set version number for internal access
    algwsym_version = 'unknown'
    try:
        from algebra_with_sympy.version import __version__ as algwsym_version
    except FileNotFoundError as e:
        UserWarning('Could not read the version.py file. Your installation'
                    ' of algebra_with_sympy probably did not work correctly.')
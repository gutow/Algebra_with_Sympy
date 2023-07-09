"""
.. include:: ../ReadMe.md
.. include:: ../Development Notes.md
"""
__docformat__ = "numpy"

from algebra_with_sympy.algebraic_equation import *

# Set config value for numerics before adjusting with the preparser
algwsym_config.numerics.integers_as_exact = False # adjusted in preparser.
from algebra_with_sympy.preparser import *

# Set the output formatting defaults
algwsym_config.output.show_code = False
algwsym_config.output.human_text = True
algwsym_config.output.label = True
algwsym_config.output.solve_to_list = False

# Set version number for internal access
algwsym_version = 'unknown'
try:
    from algebra_with_sympy.version import __version__ as algwsym_version
except FileNotFoundError as e:
    UserWarning('Could not read the version.py file. Your installation'
                ' of algebra_with_sympy probably did not work correctly.')
"""
.. include:: ../ReadMe.md
.. include:: ../Development Notes.md
"""
__docformat__ = "numpy"

from algebra_with_sympy.algebraic_equation import *
from algebra_with_sympy.preparser import *
from algebra_with_sympy.version import __version__

# Set the output formatting defaults
algwsym_config.output.show_code = False
algwsym_config.output.human_text = False
algwsym_config.output.label = True
import setuptools

# Get current script folder path so works with build
import os, sys
csfp = os.path.abspath(os.path.dirname(__file__))
if csfp not in sys.path:
    sys.path.insert(0, csfp)

try:
    from algebra_with_sympy.version import __version__
    # f = open('algebra_with_sympy/version.py','w')
    # f.write("__version__ = \"" + str(__version__) + "\"")
    # f.close()
except Exception as e:
    raise RuntimeError('Unable to find __version__') from e

setuptools.setup(
    version=__version__,
)

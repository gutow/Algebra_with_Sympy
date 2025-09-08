# Development Notes
[General](#general-notes) | [Make Docs](#constructing-the-documentation) | 
[Running Tests](#running-tests) | 
[Build PyPi Package](#building-pypi-package)|

## General Notes
<a class="anchor" href="#general-notes"></a>
* TODOs
  * Test collect when there isn't an available _eval_collect (not sure how 
    to get there).
  * Test for _binary_op NotImplemented error (not sure how to get there).
* To consider
  * Include [Sympy Plot Backends](https://sympy-plot-backends.readthedocs.io/en/latest/)
    in the default setup.
  * Change `Equation` constructor to accept `Equality`, `Set`, `List` or 
    `lhs, rhs`, rather than just `lhs, rhs`.
  * Extend `.subs` to accept `.subs(a=2*c, b = sin(q), ...)`.
  * [MathLive](https://cortexjs.io/mathlive/) on another web page as possible
    input engine.

## Constructing the Documentation
<a class="anchor" href="#constructing-the-documentation"></a>
1. Make sure pdoc is installed and updated in the virtual environment `pip 
   install -U pdoc`.
2. Update any `.md` files included in `_init_.py`.
   * Generally URLs should be absolute, not relative.
3. At the root level run pdoc 
`
pdoc --logo https://gutow.github.io/Algebra_with_Sympy/alg_w_sympy.svg 
--logo-link https://gutow.github.io/Algebra_with_Sympy/
--footer-text "Algebra with Sympy vX.X.X" --math -html -o docs 
   ./algebra_with_sympy
`
   where `X.X.X` is the version number.

### Tasks for Documentation
<a class="anchor" href="#tasks-for-documentation"></a>
* Readme.md & Development Notes.md
  * Use absolute path to github pages for more examples.

## Running Tests
<a class="anchor" href="#running-tests"></a>
1. Install updated pytest in the virtual environment:
   ```
   pipenv shell
   pip install -U pytest
   ```
2. Run standard tests:
   `pytest --ignore='Developer Testing' --ignore-glob='*test_preparser.py'`.
3. Run preparser tests:
   `ipython -m pytest tests/test_preparser.py`
4. Run doctests:
   `pytest --ignore='tests' --ignore='Developer Testing' 
   --ignore-glob='*old*' --doctest-modules`

You can run all the tests using the dotests script: `./dotests.sh`.

**NOTE**: Some warnings about invalid escape characters are expected because 
raw strings are being passed with specialized LaTex escaped characters.

## Building PyPi package
<a class="anchor" href="#building-pypi-package"></a>
1. Make sure to update the version number in setup.py first.
1. Install updated  setuptools and twine in the virtual environment:
   ```
   pipenv shell
   pip install -U setuptools wheel twine
   ```
1. Build the distribution `python -m build`.
1. Test it on `test.pypi.org`.
    1. Upload it (you will need an account on test.pypi.org):
       `python -m twine upload --repository testpypi dist/*`.
    1. Create a new virtual environment and test install into it:
        ```
        exit # to get out of the current environment
        cd <somewhere>
        mkdir <new virtual environment>
        cd <new directory>
        pipenv shell #creates the new environment and enters it.
        pip install -i https://test.pypi.org/..... # copy actual link from the
                                                   # repository on test.pypi.
        ```
       There are often install issues because sometimes only older versions of
       some of the required packages are available on test.pypi.org. If this
       is the only problem change the version to end in `rc0` for release
       candidate and try it on the regular pypi.org as described below for
       releasing on PyPi.
    1. After install test by running a jupyter notebook in the virtual 
       environment.

### Releasing on PyPi
<a class="anchor" href="#releasing-on-pypi"></a>
Proceed only if testing of the build is successful.

1. Double check the version number in `algebra_with_sympy/version.py`.
1. Rebuild the release: `python -m build`.
1. Upload it: `python -m twine upload dist/*`
1. Make sure it works by installing it in a clean virtual environment. This
   is the same as on test.pypi.org except without `-i https://test.pypy...`. If
   it does not work, pull the release.

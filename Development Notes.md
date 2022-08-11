[General](#general-notes) | [Make Docs](#constructing-the-documentation) | 
[Build PyPi Package](#building-pypi-package)|
## General Notes
* Important TODOs
  * Build generic testing of all functions in `sympy.functions.__all__`. This 
    will reveal any new functions that need special adaptations.
  * Add tests for `Equality` conversion to an `Equation`.
* To consider
  * Change `Equation` constructor to accept `Equality`, `Set`, `List` or 
    `lhs, rhs`, rather than just `lhs, rhs`.

## Constructing the Documentation

1. Make sure pdoc is installed and updated in the virtual environment `pip 
   install -U pdoc`.
2. Update any `.md` files included in `_init_.py`.
   * Generally URLs should be absolute, not relative.
3. At the root level run pdoc `pdoc 
--logo https://gutow.github.io/Algebra_with_Sympy/alg_w_sympy.svg
--logo-link https://gutow.github.io/Algebra_with_Sympy/
--footer-text "Algebra with Sympy vX.X.X" --math -html -o docs algebra_with_sympy` 
   where `X.X.X` is the version number.

### Tasks for Documentation
* Readme.md & intro.md
  * Hard code anchors so that navigation links work on pypi page.
  * Use absolute path to github pages for more examples.

## Building PyPi package

1. Make sure to update the version number in setup.py first.
1. Install updated  setuptools and twine in the virtual environment:
   ```
   pipenv shell
   pip install -U setuptools wheel twine
   ```
1. Build the distribution `python -m setup sdist bdist_wheel`.
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

Proceed only if testing of the build is successful.

1. Double check the version number in setup.py.
1. Rebuild the release: `python -m setup sdist bdist_wheel`.
1. Upload it: `python -m twine upload dist/*`
1. Make sure it works by installing it in a clean virtual environment. This
   is the same as on test.pypi.org except without `-i https://test.pypy...`. If
   it does not work, pull the release.

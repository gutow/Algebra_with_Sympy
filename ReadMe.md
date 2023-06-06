# Algebraic Equations with SymPy

[Introduction](#introduction) | [Output Formatting](#controlling-the-format-of-interactive-outputs)
| [Installation](#setupinstallation) |
[Try Live](#try-in-binder) | [Issues or Comments](#issues-or-comments) |
[Change Log](#change-log) |
[License](#licensed-under-gnu-v3-licensehttpsgnuorglicenses)
| [GIT Repository](https://github.com/gutow/Algebra_with_Sympy)
| [PyPi Link](https://pypi.org/project/Algebra-with-SymPy/)

## [Website/Documentation (including API)](https://gutow.github.io/Algebra_with_Sympy/)

## Introduction

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
over missed details such as a negative sign.

A simple example as it would appear in a [Jupyter](https://jupyter.org) 
notebook is shown immediately below:

![screenshot of simple example](https://gutow.github.io/Algebra_with_Sympy/resources/simple_example.png)

The last cell illustrates how it is possible to substitute numbers with 
units into the solved equation to calculate a numerical solution with 
proper units.

In IPython environments (IPython and Jupyter) there is also a shorthand 
syntax for entering equations provided through the IPython preparser. An 
equation can be specified as `eq1 =@ a/b = c/d`.


![screenshot of short syntax](https://gutow.github.io/Algebra_with_Sympy/resources/short_syntax.png)

If no Python name is 
specified for the equation (no `eq_name` to the left of `=@`), the equation 
will still be defined, but will not be easily accessible for further 
computation. The `=@` symbol combination was chosen to avoid conflicts with 
reserved python  symbols while minimizing impacts on syntax highlighting 
and autoformatting.

[More examples of the capabilities of Algebra with Sympy are 
here](https://gutow.github.io/Algebra_with_Sympy/Demonstration%20of%20equation%20class.html).

Many math packages such as [SageMath](https://www.sagemath.org/) 
and [Maxima](http://maxima.sourceforge.net/) have similar capabilities, 
but require more knowledge of command syntax, plus they cannot easily be 
installed in a generic python environment.

## Controlling the Format of Interactive Outputs
* These controls impact all Sympy objects and the `Equation` class.
* **In graphical environments (Jupyter)** you will get rendered Latex such as 
$\frac{a}{b} = \frac{c}{d}$ or $e^{\frac{-x^2}{\sigma^2}}$. To also see the 
  code representation (what can be copied and pasted for 
  additional computation) set `algwsym_config.output.show_code = True`. 
  This will print the code version (e.g. `Equation(a,b/c)`) of equations 
  and sympy expression in addition to the human readable version. This code 
  version can be accessed directly by calling `repr()` on the 
  equation or expression.

* **In interactive text environments (IPython and command line)** The human 
  readable string version of Sympy expressions are returned (for `Equations` a 
  = b rather than Equation(a,b)). This is equivalent to Calling `print()` 
  or `str()` on an expression. 
  * To have the code version (can be copied and pasted as a 
    Python statement) returned, set `algwsym_config.output.human_text = False`.
  * Setting both `algwsym_config.output.human_text = True`
    and `algwsym_config.output.show_code = True`, will return both the 
    code and human readable versions.

* **The equation label** can be turned off by setting
  `algwsym_config.output.label = False`.

* By default **solutions output by `solve()`** are returned as a SymPy 
  `FiniteSet()` to force typesetting of the included solutions. To get Python 
  lists instead you can override this for the whole session by setting
  `algwsym_config.output.solve_to_list = True`. For a one-off, simply 
  wrap the output of a solve in `list()` (e.g. `list(solve(...))`).

## Setup/Installation

1. Use pip to install in your python environment: 
`pip install -U Algebra-with-SymPy`
2. To use in a running python session issue
the following command : `from algebra_with_sympy import *`. 
This will also import the SymPy tools. 
3. If you want to isolate this tool from the global namespace you are 
   working with change the import statement 
to `import algebra_with_sympy as spa`, where 
`spa` stands for "SymPy Algebra". Then all calls would be made to `
spa.funcname()`.

## Try in binder

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/gutow/Algebra_with_Sympy.git/master/?filepath=Demonstration%20of%20equation%20class.ipynb)

## Issues or Comments

* Issues and bug reports should be [filed on 
github](https://github.com/gutow/Algebra_with_Sympy/issues).
* Comments, questions, show and tell, etc. should go in the [project 
  discussions](https://github.com/gutow/Algebra_with_Sympy/discussions).

## Change Log

* 0.11.0dev (June 5, 2023)
  * Formatting of `FiniteSets` overridden so that the contents always
    pretty-print. This removes the necessity of special flags to get 
    pretty output from `solve`.
  * Sympy `solve()` now works reliably with equations and outputs 
    pretty-printed solutions.
  * Added option `algwsym_config.output.solve_to_list = True` which causes 
    `solve()` to return solutions sets as Python lists. Using this option 
    prevents pretty-printing of the solutions produced by `solve()`.
  * `algwsym_config.output.show_code` and 
    `algwsym_config.output.human_text` now work for all sympy objects, not 
    just `Equation` objects. This works
    in terminal, IPython terminal and Jupyter. This is achieved by hooking 
    into the python `display_hook` and IPython `display_formatter`.
  * Added jupyter to requirements.txt so that virtual environment builds
    will include jupyter.
  * The way `__version__` was handled could break pip install. Changed to
    generating the internal version during setup. This means the version
    is now available as `algwsym_version`.
* 0.10.0 (Sep. 5, 2022)
  * Documentation updates and fixes.
  * Significantly increased test coverage (~98%).
  * Support for `Eqn.rewrite(Add)`
  * Solving (e.g. `solve(Eqn,x)`) now supported fully. Still experimental.
  * Bug fix: latex printing now supports custom printer.
  * Substitution into an Equation using Equations is now 
    supported (e.g. `eq1.subs(eq2, eq3, ...)`).
  * `algebra_with_sympy.__version__` is now available for version checking 
    within python.
  * Bug fix: preparsing for `=@` syntax no longer blocks `obj?` syntax for 
    getting docstrings in ipython.
  * More robust determination of equation names for labeling.
* 0.9.4 (Aug. 11, 2022)
  * Update to deal with new Sympy function `piecewise_exclusive` in v1.11.
  * Added user warning if a function does not extend for use with `Equations` 
    as expected. This also allows the package to be used even when a function 
    extension does fail.
  * Simplification of documentation preparation.
  * Typo fixes in preparser error messages.
* 0.9.3 (Aug. 9, 2022)
  * Added check for new enough version of IPython to use the preparser.
  * If IPython version too old, issue warning and do not accept `=@` shorthand.
* 0.9.2 (Jun. 5, 2022)
  * `=@` shorthand syntax for defining equations in IPython compatible 
    environments.
  * Fixed bug where `root()` override called `sqrt()` on bare expressions.
* 0.9.1 (Mar. 24, 2022)
  * Equations labeled with their python name, if they have one.
  * Added flags to adjust human readable output and equation labeling.
  * Accept equation as function argument in any position.
  * First pass at `solve()` accepting equations.
  * Added override of `root()` to avoid warning messages.
  * More unit tests.
  * First pass at documentation.
* 0.9.0 functionality equivalent to extension of SymPy in
[PR#21333](https://github.com/sympy/sympy/pull/21333).

## [licensed under GNU V3 license](https://gnu.org/licenses)

This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

Copyright - Algebra with Sympy Contributors 2021, 2022, 2023
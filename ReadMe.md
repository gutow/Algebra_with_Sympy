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
<a class="anchor" href="#introduction"></a>

This tool defines relations that all high school and college students would
recognize as mathematical equations. 
They consist of a left hand side (lhs) and a right hand side (rhs) connected by
the relation operator "=". In addition, it sets some convenient defaults and 
provides some controls of output formatting that may be useful even if
you do not use the `Equation` class (see [Conveniences for
SymPy](#convenience-tools-and-defaults-for-interactive-use-of-sympy)).

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
proper units. The `units(...)` operation is part this package, not Sympy.

In IPython environments (IPython, Jupyter, Google  Colab, etc...) there is 
also a shorthand syntax for entering equations provided through the IPython 
preparser. An equation can be specified as `eq1 =@ a/b = c/d`.


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

## Convenience Tools and Defaults for Interactive Use of SymPy

Even if you do not use the `Equation` class, there are some convenience 
tools and defaults that will probably make interactive use of SymPy in 
Jupyter/IPython environments easier:

* By default, all numbers *in Sympy expressions* without decimal points are 
  interpreted as integers (e.g. `2/3*x`, where x is a sympy symbol, -> 
  `2*x/3` not `x*0.6666...`, but if x is just a plain Python object then `2/3*x` 
  -> `x*0.66666...`). This can be turned off with `unset_integers_as_exact()`, 
  which leads to standard Python behavior (`2/3*x` -> `x*0.6666...`) even for 
  Sympy expressions. Turn on with `set_integers_as_exact()`. When on the flag
  `algwsym_config.numerics.integers_as_exact = True`.
* Results of `solve()` are wrapped in `FiniteSet()` to force pretty-printing 
  of all of a solution set. See [Controlling the Format of Interactive 
  Outputs](#controlling-the-format-of-interactive-outputs).
* It is possible to set the default display to show both the pretty-printed 
  result and the code version simultaneously. See [Controlling the Format of Interactive 
  Outputs](#controlling-the-format-of-interactive-outputs).  

## Controlling the Format of Interactive Outputs
<a class="anchor" href="#controlling-the-format-of-interative-outputs"></a>
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

* **Automatic wrapping of `Equations` as Latex equations** can be activated 
  by  setting `algwsym_config.output.latex_as_equations` to `True`. The 
  default is `False`. Setting this to `True` wraps output as LaTex equations,
  wrapping them in `\begin{equation}...\end{equation}`. Equations formatted 
  this way will **not** be labeled with the internal name for the equation, 
  independent of the setting of `algwsym_config.output.label`.

* By default **solutions output by `solve()`** are returned as a SymPy 
  `FiniteSet()` to force typesetting of the included solutions. To get Python 
  lists instead you can override this for the whole session by setting
  `algwsym_config.output.solve_to_list = True`. For a one-off, simply 
  wrap the output of a solve in `list()` (e.g. `list(solve(...))`). One 
  advantage of list mode is that lists can be ordered. When
  `algwsym_config.output.solve_to_list = True` `solve()` maintains the 
  solutions in the order the solve for variables were input.

## Setup/Installation
<a class="anchor" href="#setupinstallation"></a>
1. Use pip to install in your python environment: 
`pip install -U Algebra-with-SymPy`
2. To use in a running python session issue
the following command : `from algebra_with_sympy import *`. 
This will also import the SymPy tools. 
3. If you want to isolate this tool from the global namespace you are 
   working with change the import statement 
to `import algebra_with_sympy as spa`, where 
`spa` stands for "SymPy Algebra". Then all calls would be made to `
spa.funcname()`. WARNING: Doing this makes shorthand equation input and 
   control of interactive output formats unavailable. To recover this 
   functionality the following code must be run in the interactive session.
```
Equation = spa.Equation
Eqn = Equation
algwsym_config = spa.algwsym_config
```

## Try in binder
<a class="anchor" href="#try-in-binder"></a>
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/gutow/Algebra_with_Sympy.git/master?labpath=Demonstration+of+equation+class.ipynb)

## Issues or Comments
<a class="anchor" href="#issues-or-comments"></a>
* Issues and bug reports should be [filed on 
github](https://github.com/gutow/Algebra_with_Sympy/issues).
* Comments, questions, show and tell, etc. should go in the [project 
  discussions](https://github.com/gutow/Algebra_with_Sympy/discussions).

## Change Log
<a class="anchor" href="#change-log"></a>
* 1.1.3 (September 7, 2025)
  * Better checking for an incompatible sympy installation and improved 
    warning on how to solve the problem.
  * Shifting to more modern `pyproject.toml` packaging.
  * Updates to Developer documentation to reflect packaging changes.
  * Moved determination of equation (actually any sympy basic object) python 
    name to this package from the equation object, thus simplifying what is 
    included in sympy.
  * Minor test updates.
  * Added overrides of __repr__ and __str__ in preparation for inclusion of 
    Equation class in Sympy.
* 1.1.2 (August 13, 2024)
  * Test updates.
  * Verified compatibility with Sympy 1.13.2.
* 1.1.1 (July 25, 2024)
  * BUG FIX accommodate empty re.search results in preparser. Prevents 
    unnecessary error messages.
* 1.1.0 (July 22, 2024)
  * Setting integers as exact (`set_integers_as_exact()`, the default) now 
    only sets integers as exact within Sympy and Algebra_with_Sympy 
    expressions. This increases compatibility with other packages that 
    depend on integers being Python integers.
  * Refuse to import Algebra_with_Sympy if an incompatible 
    version of Sympy is installed in the environment.
  * Added warning explaining how to install a compatible version of Sympy.
* 1.0.2 (July 5, 2024)
  * Removed requirements for Jupyter and Jupyterlab as code will work in 
    vanilla python or Google Colab.
  * Workaround for Google Colab's inconsistent handling of mixed Latex and 
    plain text strings. This impacted display of equation labels in Colab.
  * BUG FIX: catch IPython not installed so that can run in plain vanilla 
    python.
* 1.0.1 (May 22, 2024)
  * BUG FIX: equation labels that include underscore characters "_" are now 
    accepted.
  * BUG FIX: wrapping equations formatted as LaTex equation (ie. surrounded 
    by `\begin{equation}...\end{equation}`) in the `$..$` code used to 
    indicate markdown for MathJax was causing output errors in Quarto when 
    outputing to .tex or .pdf. This is now fixed without negatively 
    impacting MathJax rendering.
  * BUG FIX: Singleton results of solve unnecessarily wrapped by extra list 
    or finiteset. No longer double nested.
  * BUG FIX: When returning lists make solve respect user order of solutions.
  * BUG FIX: Equation output threw error when Algebra_with_Sympy was 
    imported as a submodule. Equation labeling turned off for this type of 
    import to avoid error.
  * BUG FIX: Equation labels are now copyable even with the newer MathJax 
    commonHTML rendering.
  * Updates to requirements.txt.
  * Documentation updates.
* 1.0.0 (January 2, 2024)
  * Added convenience operation `units(...)` which takes a string of space 
    separated symbols to use as units. This simply declares the symbols 
    to be positive, making them behave as units. This does not create units 
    that know about conversions, prefixes or systems of units. This lack 
    is on purpose to provide units that require the user to worry about 
    conversions (ideal in a teaching situation). To get units with built-in 
    conversions see `sympy.physics.units`.
  * Fixed issue #23 where `cos()` multiplied by a factor was not the same 
    type of object after `simplify()` acted on an expression. Required 
    embedding the `Equation` type in the sympy library. Until `Equation` is 
    incorporated into the primary Sympy repository a customized version of 
    the latest stable release will be used.
  * Fixed issue where trailing comments (ie. `# a comment` at the end of a 
    line) lead to input errors using compact `=@` notation.
  * `algwsym_config.output.latex_as_equations` has a default value of `False`.
     Setting this to `True` wraps output as LaTex equations wrapping them 
    in `\begin{equation}...\end{equation}`. Equations formatted this way 
    will not be labeled with the internal name for the equation.
* 0.12.0 (July 12, 2023)
  * Now defaults to interpreting numbers without decimal points as integers. 
    This can be turned off with `unset_integers_as_exact()` and on with
    `set_integers_as_exact()`. When on the flag
    `algwsym_config.numerics.integers_as_exact = True`.
* 0.11.0 (June 5, 2023)
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
<a class="anchor" href="#licensed-under-gnu-v3-licensehttpsgnuorglicenses"></a>
This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

Copyright - Algebra with Sympy Contributors 2021, 2022, 2023, 2024
def algebra_with_sympy_preparser(lines):
    """
    In IPython compatible environments (Jupyter, IPython, etc...) this supports
    a special compact input method for equations.

    The syntax supported is `equation_name =@ equation.lhs = equation.rhs`,
    where `equation_name` is a valid Python name that can be used to refer to
    the equation later. `equation.lhs` is the left-hand side of the equation
    and `equation.rhs` is the right-hand side of the equation. Each side of the
    equation must parse into a valid Sympy expression.

    **Note**: This does not support line continuation. Long equations should be
    built by combining expressions using names short enough to do this on one
    line. The alternative is to use `equation_name = Eqn(long ...
    expressions ... with ... multiple ... lines)`.

    **Note**: If the `equation_name` is omitted the equation will be formed,
    but it will not be assigned to a name that can be used to refer to it
    later. You may be able to access it through one of the special IPython
    underscore names. This is not recommended.

    **THIS FUNCTION IS USED BY THE IPYTHON ENVIRONMENT TO PREPARSE THE INPUT
    BEFORE IT IS PASSED TO THE PYTHON INTERPRETER. IT IS NOT MEANT TO BE USED
    DIRECTLY BY A USER**
    """
    new_lines = []
    if isinstance(lines,str):
        lines = [lines]
    for k in lines:
        if '=@' in k:
            drop_comments = k.split('#')
            to_rephrase = ''
            if len(drop_comments) > 2:
                for i in range(len(drop_comments)-1):
                    to_rephrase += drop_comments[i]
            else:
                to_rephrase = drop_comments[0]
            linesplit = to_rephrase.split('=@')
            eqsplit = linesplit[1].split('=')
            if len(eqsplit)!=2:
                raise ValueError('The two sides of the equation must be' \
                                 ' separated by an \"=\" sign when using' \
                                 ' the \"=@\" special input method.')
            templine =''
            if eqsplit[0]!='' and eqsplit[1]!='':
                if eqsplit[1].endswith('\n'):
                    eqsplit[1] = eqsplit[1][:-1]
                if linesplit[0]!='':
                    templine = str(linesplit[0])+'= Eqn('+str(eqsplit[0])+',' \
                        ''+str(eqsplit[1])+')\n'
                else:
                    templine = 'Eqn('+str(eqsplit[0])+','+str(eqsplit[1])+')\n'
            new_lines.append(templine)
        else:
            new_lines.append(k)
    return new_lines


def integers_as_exact(lines):
    """This preparser uses `sympy.interactive.session.int_to_Integer` to
    convert numbers without decimal points into sympy integers so that math
    on them will be exact rather than defaulting to floating point. **This
    should not be called directly by the user. It is plugged into the
    IPython preparsing sequence when the feature is requested.** The default for
    Algebra_with_sympy is to use this preparser. This can be turned on and
    off using the Algebra_with_sympy functions:
    * `set_integers_as_exact()`
    * `unset_integers_as_exact()`
    """
    from sympy.interactive.session import int_to_Integer
    string = ''
    for k in lines:
        string += k + '\n'
    string = string[:-1] # remove the last '\n'
    return int_to_Integer(string)

from IPython import get_ipython
if get_ipython():
    if hasattr(get_ipython(),'input_transformers_cleanup'):
        get_ipython().input_transformers_post.\
            append(algebra_with_sympy_preparser)
    else:
        import warnings
        warnings.warn('Compact equation input unavailable.\nYou will have ' \
                      'to use the form "eq1 = Eqn(lhs,rhs)" instead of ' \
                      '"eq1=@lhs=rhs".\nIt appears you are running an ' \
                      'outdated version of IPython.\nTo fix, update IPython ' \
                      'using "pip install -U IPython".')
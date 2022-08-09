def algebra_with_sympy_preparser(lines):
    """
    In IPython compatible environments (Jupyter, IPython, etc...) this supports
    a special compact input method for equations.

    The syntax supported is `equation_name =@ equation.lhs = equation.rhs`,
    where `equation_name` is a valid Python name that can be used to refer to
    the equation later. `equation.lhs` is the left-hand side of the equation
    and `equation.rhs` is the right-hand side of the equation. Each side of the
    equation must parse into a valid Sympy expression.

    **Note**: If the `equation_name` is omitted the equation will be formed,
    but it will
    not be assigned to a name that can be used to refer to it later. You may be
    able to access it through one of the special IPython underscore names. This
    is not recommended.

    **THIS FUNCTION IS USED BY THE IPYTHON ENVIRONMENT TO PREPARSE THE INPUT
    BEFORE IT IS PASSED TO THE PYTHON INTERPRETER. IT IS NOT MEANT TO BE USED
    DIRECTLY BY A USER**
    """
    new_lines = []
    for k in lines:
        if '=@' in k:
            linesplit = k.split('=@')
            eqsplit = linesplit[1].split('=')
            if len(eqsplit)!=2:
                raise ValueError('The two sides of the equation must be' \
                                 ' separated by an \"=\" sign when using' \
                                 ' the \"=*\" special input method.')
            templine =''
            if eqsplit[0]!='' and eqsplit[1]!='':
                if linesplit[0]!='':
                    templine = str(linesplit[0])+'=Eqn('+str(eqsplit[0])+',' \
                        ''+str(eqsplit[1])+')\n'
                else:
                    templine = 'Eqn('+str(eqsplit[0])+','+str(eqsplit[1])+')\n'
            new_lines.append(templine)
        else:
            new_lines.append(k+'\n')
    return(new_lines)

from IPython import get_ipython
if get_ipython():
    if hasattr(get_ipython(),'input_transformers_cleanup'):
        get_ipython().input_transformers_cleanup.\
            append(algebra_with_sympy_preparser)
    else:
        import warnings
        warnings.warn('Compact equation input unavailable.\nYou will have ' \
                      'to use the form "eq1 = Eqn(lhs,rhs)" instead of ' \
                      '"eq1=@lhs=rhs".\nIt appears you are running an ' \
                      'outdated version of IPython.\nTo fix, update IPython ' \
                      'using "pip install -U IPython".')
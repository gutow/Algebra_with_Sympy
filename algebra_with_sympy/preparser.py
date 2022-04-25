def algebra_with_sympy_preparser(lines):
    """
    In IPython compatible environments (Jupyter, IPython, etc...) this supports
    a special compact input method for equations.

    The syntax supported is `equation_name=:equation.lhs = equation.rhs`,
    where `equation_name` is a valid Python name that can be used to refer to
    the equation later. `equation.lhs` is the left-hand side of the equation
    and `equation.rhs` is the right-hand side of the equation. Each side of the
    equation must parse into a valid Sympy expression.
    """
    new_lines = []
    for k in lines:
        if '=:' in k:
            linesplit = k.split('=:')
            eqsplit = linesplit[1].split('=')
            if len(eqsplit)!=2:
                raise ValueError('The two sides of the equation must be' \
                                 ' separated by an \"=\" sign when using' \
                                 ' the \"=:\" special input method.')
            templine =''
            if eqsplit[0]!='' and eqsplit[1]!='':
                if linesplit[0]!='':
                    templine = str(linesplit[0])+'=Eqn('+str(eqsplit[0])+',' \
                        ''+str(eqsplit[1])+')\n'
                else:
                    templine = 'Eqn('+str(eqsplit[0])+','+str(eqsplit[1])+')\n'
            new_lines.append(templine)
        else:
            new_lines.append(k)
    return(new_lines)

from IPython import get_ipython
get_ipython().input_transformers_cleanup.append(algebra_with_sympy_preparser)

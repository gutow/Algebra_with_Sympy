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


def toIntegerInSympyExpr(string):
    """ This function takes a string of valid Python and wraps integers within Sympy expressions
        in `sympy.Integer()` to make them Sympy integers rather than Python `Int()`. The
        advantage of this is that calculations with `Integer()` types can be exact. This function
        is careful not to wrap `Int()` types that are not part of Sympy expressions, making it
        possible for this functionality to exist with operations (e.g. array and numpy indexing)
        that are not compatible with the `Integer()` type.
    """
    from tokenize import generate_tokens, NEWLINE, OP, untokenize
    from io import StringIO
    ###
    # Internally used functions
    ###
    def isSympy(tokens, newSymObj):
        """ Checks list of tokens to see if it contains a Sympy Object

        Parameters
        ==========
        tokens:list of tokens.
        newSymObj:list of string names of Sympy objects that have been declared
          in the current script/string being parsed.
        """
        from sympy import Basic
        from tokenize import NAME
        import __main__ as user_ns
        # print(dir(user_ns))
        sympy_obj = False
        for kind, string, start, end, line in tokens:
            if kind == NAME:
                # print('Checking: '+str(string))
                if hasattr(user_ns, string):
                    if isinstance(getattr(user_ns, string), Basic):
                        sympy_obj = True
                if string in newSymObj:
                    sympy_obj = True
        return sympy_obj

    def toSympInteger(tokens):
        from tokenize import NUMBER, OP, NAME
        result = []
        for k in tokens:
            if k[0] != NUMBER:
                result.append((k[0], k[1]))
            else:
                if '.' in k[1] or 'j' in k[1].lower() or 'e' in k[1].lower():
                    result.append((k[0], k[1]))
                else:
                    result.extend([
                        (NAME, 'Integer'),
                        (OP, '('),
                        (NUMBER, k[1]),
                        (OP, ')')
                    ])
        return result

    def checkforSymObjDecl(token):
        import re
        from tokenize import NAME
        syms = []
        for kind, string, start, end, line in token:
            if kind == NAME:
                if string == 'var':
                    match = re.search(r'\".*?\"|\'.*?\'', line)
                    syms = match.group().replace('\"', '').replace('\'',
                                                                   '').split(
                        ' ')
                if string == 'units':
                    match = re.search(r'\".*?\"|\'.*?\'', line)
                    syms = match.group().replace('\"', '').replace('\'',
                                                                   '').split(
                        ' ')
                if string == 'symbols':
                    parts = line.split('=')
                    syms = parts[0].replace(' ', '').split(',')
                if string == 'Symbol':
                    parts = line.split('=')
                    syms = parts[0].replace(' ', '').split(',')
        return syms

    ###
    # The parsing and substitution.
    ###
    g = generate_tokens(StringIO(string).readline)
    declaredSymObj = []
    result = []
    temptokens = []
    openleft = 0
    for k in g:
        declaredSymObj.extend(checkforSymObjDecl([k]))
        temptokens.append(k)
        if k[0] == OP and k[1] == '(':
            openleft += 1
        if k[0] == OP and k[1] == ')':
            openleft -= 1
        if k[0] == NEWLINE and openleft == 0:
            # This is where we check for sympy objects and replace int() with Integer()
            hasSympyObj = isSympy(temptokens, declaredSymObj)
            if hasSympyObj:
                converted = toSympInteger(temptokens)
                result.extend(converted)
            else:
                result.extend(temptokens)
            temptokens = []
    return untokenize(result)

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
    NOTE: This option does not work in plain vanilla Python sessions. You
    must be running in an IPython environment (Jupyter, Notebook, Colab,
    etc...).
    """
    #from sympy.interactive.session import int_to_Integer
    string = ''
    for k in lines:
        string += k + '\n'
    string = string[:-1] # remove the last '\n'
    return toIntegerInSympyExpr(string)
try:
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
except ModuleNotFoundError:
    pass
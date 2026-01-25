###
# Utility functions
###

from sympy.core.basic import Basic

def _get_user_ns():
    """
    Returns the module `__main__` or None, if it cannot be found.
    """
    user_namespace = None
    try:
        import __main__ as user_namespace
    except ModuleNotFoundError:
        pass
    return user_namespace

def __get_algwsym_config():
    """
    Tries to find the object `algwsym_config` in the user_namespace (
    __main__). Returns the object or None.
    """
    user_namespace = _get_user_ns()
    if hasattr(user_namespace, 'algwsym_config'):
        algwsym_config = getattr(user_namespace, 'algwsym_config')
        return algwsym_config
    else:
        return None

def __get_sympy_expr_name__(expr):
    """
    Tries to find the python string name that refers to a sympy object. Looks
    in __main__. Historically also needed to look in the IPython user_ns,
    but that no longer seems to be true.
    :return: string value if found or empty string.
    """
    import __main__ as shell
    for k in dir(shell):
        item = getattr(shell, k)
        if isinstance(item, Basic):
            if item == expr and not k.startswith('_'):
                return k
    return ''

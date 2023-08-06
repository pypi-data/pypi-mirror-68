'''

Jinja Result Parsing - converts str(dict) => dict

Taken from ansible:
https://github.com/ansible/ansible/blob/308723c3ca1122363e419070f1fa1d76ff5611a9/lib/ansible/template/safe_eval.py

'''

import ast
import sys
from six import string_types
from six.moves import builtins
from .util import InvalidExpression, CircularReference

# from ansible import constants as C
# from ansible.plugins.loader import filter_loader, test_loader

# define certain JSON types
# eg. JSON booleans are unknown to python eval()
OUR_GLOBALS = {
    '__builtins__': {},  # avoid global builtins as per eval docs
    'true': True, 'false': False, 'null': None,
    'True': True, 'False': False, 'None': None,
}

# this is the whitelist of AST nodes we are going to
# allow in the evaluation.
SAFE_NODES = set((
    ast.Add,
    ast.BinOp,
    ast.Compare,
    ast.Dict,
    ast.Div,
    ast.Expression,
    ast.List,
    ast.Load,
    ast.Mult,
    ast.Num,
    ast.Name,
    ast.Set,
    ast.Str,
    ast.Sub,
    ast.USub,
    ast.Tuple,
    ast.UnaryOp,
))

# And in Python 3.6 too, although not encountered until Python 3.8, see https://bugs.python.org/issue32892
if sys.version_info[:2] >= (3, 4):
    SAFE_NODES.add(ast.NameConstant)
if sys.version_info[:2] >= (3, 6):
    SAFE_NODES.add(ast.Constant)

class CleansingNodeVisitor(ast.NodeVisitor):
    def __init__(self, whitelist=None, *a, **kw):
        self.whitelist = whitelist

    def generic_visit(self, node, inside_call=False):
        if type(node) not in SAFE_NODES:
            raise InvalidExpression()
        if isinstance(node, ast.Call):
            inside_call = True
        elif self.whitelist is not None and isinstance(node, ast.Name) and inside_call:
            # Disallow calls to builtin functions that we have not vetted
            # as safe.  Other functions are excluded by setting locals in
            # the call to eval() later on iterate over all child nodes
            if hasattr(builtins, node.id) and node.id not in self.whitelist:
                raise Exception("invalid function: %s" % node.id)

        for child_node in ast.iter_child_nodes(node):
            self.generic_visit(child_node, inside_call)


def safe_eval(expr, locals=None, circular=[]):
    '''
    This is intended for allowing things like:
    with_items: a_list_variable
    Where Jinja2 would return a string but we do not want to allow it to
    call functions (outside of Jinja2, where the env is constrained).
    Based on:
    http://stackoverflow.com/questions/12523516/using-ast-and-whitelists-to-make-pythons-eval-safe
    '''
    locals = {} if locals is None else locals
    if not isinstance(expr, string_types): # already templated to a datastructure, perhaps?
        return expr

    # filter_list = []
    # for filter_ in filter_loader.all():
    #     filter_list.extend(filter_.filters().keys())
    #
    # test_list = []
    # for test in test_loader.all():
    #     test_list.extend(test.tests().keys())
    #
    # CALL_WHITELIST = C.DEFAULT_CALLABLE_WHITELIST + filter_list + test_list
    cnv = CleansingNodeVisitor() # CALL_WHITELIST
    try:
        parsed_tree = ast.parse(expr, mode='eval')
        cnv.visit(parsed_tree)
        # Note: passing our own globals and locals here constrains what
        # callables (and other identifiers) are recognized.  this is in
        # addition to the filtering of builtins done in CleansingNodeVisitor
        return eval(compile(parsed_tree, expr, 'eval'), OUR_GLOBALS, dict(locals))
    except InvalidExpression:
        raise InvalidExpression("invalid expression ({})".format(expr)) from e
    except Exception as e:
        return expr

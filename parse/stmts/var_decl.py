from parse.stmts.stmt import Stmt
import parse
import enum

from parse.token import Token

class TypeSignSpecifier(enum.Enum):
    SIGNED = 0
    UNSIGNED = 1
    UNSPECIFIED = 2

# a reference to a var (as in "... = x + 2", not a
#   pointer-related reference)
class VarRef(object):
    def __init__(self, specifier : TypeSignSpecifier, type, varName : Token,
            value = None):

        super().__init__()

        self.specifier = specifier
        self.type = type
        self.value = value

class VarDecl(Stmt):
    def __init__(self):

        super().__init__()

        # a single "var" keyword may define multiple variables via
        #   usage of , 
        # e.g. "var i8 a, i32 b"
        self.vars = list()

    def addVar(self, var : VarRef):
        self.vars.append(var)
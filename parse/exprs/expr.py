from parse.token import Token
from parse.scope import Scope

class Expr(object):
    pass

# binary expression
class Binary(Expr):
    def __init__(self, oper : Token, leftOpd : Expr, rightOpd : Expr):
        super().__init__()

        # token of operator
        self.oper = oper

        # left operand
        self.leftOpd = leftOpd

        # right operand
        self.rightOpd = rightOpd

class Unary(Expr):
    def __init__(self, oper : Token, opd : Expr):
        super().__init__()

        # operator token
        self.oper = oper

        # operand expression
        self.opd = opd
        
# parenthesis
class Grouping(Expr):
    def __init__(self, openParen : Token, closeParen : Token, inside : Expr):
        super().__init__()

        # token of opening paren (
        self.openParen = openParen

        # token of closing paren )
        self.closeParen = closeParen

        # expression inside parens
        self.inside = inside

class Literal(Expr):
    def __init__(self, oper : Token):
        super().__init__()

        # token of literal
        self.oper = oper

# used when referencing a variable in an expression. Not called "VarReference"
#  since it's not an actual reference
class VarCall(Expr):
    def __init__(self, varName : Token, curScope : Scope):
        super().__init__()

        # the actual token of the var name
        self.varName = None
        
        # first token denoting the type of the var
        self.typeOper = None

        # the AST node where this var was declared
        self.varDecl = None
from parse.stmts.stmt import Stmt
from parse.exprs.expr import Expr

# statement expression - statement just containing an expression
class StmtExpr(Stmt):
    def __init__(self):
        self.expr : Expr = None

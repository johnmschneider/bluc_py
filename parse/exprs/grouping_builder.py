from parse.exprs.expr import Expr, Grouping
from parse.token import Token

class GBuilder(object):
    openParen : Token
    closeParen : Token
    inside : Expr

    def build(self) -> Grouping:
        return Grouping(self.openParen, self.closeParen, self.inside)
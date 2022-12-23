from parse.stmts import Block
from parse.exprs import Expr

class If(Block):
    def __init__(self) -> None:
        super().__init__()

        self.cond : Expr
        self.elseIfs : ElseIf = []

        # not every if has an else so this might validly remain as "None"
        self.else_ : Else = None

class ElseIf(Block):
    def __init__(self) -> None:
        super().__init__()
        
        # the "if" that this else-if is attached to
        self.parentStmt : If

        # condition inside the else-if
        self.cond : Expr

    def needsExtraSpace(self):
        return False

class Else(Block):
    def __init__(self) -> None:
        super().__init__()
        
        self.parentStmt : If

    def needsExtraSpace(self):
        return False
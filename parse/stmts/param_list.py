from parse.stmts import VarDecl
from parse.stmts import Stmt

class ParamList(Stmt):
    def __init__(self):
        super().__init__()
        
        self.params : VarDecl = []
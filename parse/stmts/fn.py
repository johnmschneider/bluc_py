from parse.stmts import Block
from parse.stmts import VarDecl
from parse.stmts import ParamList
from parse import Token

class Fn(Block):

    def __init__(self) -> None:
        super().__init__()
        
        self.returnType : VarDecl
        self.paramList : ParamList
        self.funcName : Token
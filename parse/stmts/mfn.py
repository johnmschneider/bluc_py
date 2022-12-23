from parse.stmts import Fn
from parse.parser import Parser

# member func/method
class Mfn(Fn):
    def __init__(self) -> None:
        super().__init__()
        
        self.class_ : ClassDef
        self.mangledName : str
        self.parser : Parser


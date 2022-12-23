from parse.stmts import Stmt

class Block(Stmt):

    def __init__(self) -> None:
        super().__init__()

        # list of statements in the body of the block
        self.body = []

    def addStmt(self, stmt : Stmt):
        self.body.append(stmt)

    # whether or not the C output needs an extra space after the block
    def needsExtraSpace(self):
        return True

    # do we even need this?
    #def __eq__(self, o: object) -> bool:
    #    return super().__eq__(o)
    #
    #def __ne__(self, o: object) -> bool:
    #    return not self.__eq__(o)
class Stmt(object):
    def __init__(self) -> None:
        super().__init__()

        # Line number that the statement starts on
        self.startLineNumber = -1
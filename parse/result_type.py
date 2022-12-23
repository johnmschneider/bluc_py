from parse.token import Token
from parse.result import Result

class ResultType(Result):
    from parse.token import Token

    def __init__(self) -> None:
        super().__init__()

        self.successful : bool  = False
        self.data               = None

        # Where the error occurred (if an error occurred)
        self.errToken : Token   = None
        self.errCode            = None

    def setData(self, data):
        self.data = data
        self.successful = True

        # to use builder-like pattern
        return self

    # shallow copy result's error and/or data
    #   to this ResultType
    def setErrFromResult(self, result):
        self.successful = result.successful
        self.data = result.data

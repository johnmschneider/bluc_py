from parse.token import Token


class Result(object):
    from parse.token import Token

    def __init__(self) -> None:
        super().__init__()

        self.successful : bool = True

        # Where the error occurred in source file (if an error occurred)
        self.errToken : Token   = None
        self.errCode            = None


    def setErrToken(self, errToken : Token):
        self.errToken = errToken
        self.successful = False

        # to use builder-like pattern
        return self

    def setErrCode(self, errCode):
        self.errCode = errCode
        self.successful = False

        # to use builder-like pattern

    # set both the error token and error code.
    def setError(self, errToken : Token, errCode):
        self.setErrToken(errToken)
        self.setErrCode(errCode)

    # returns if this result failed
    def failed(self):
        return not self.successful
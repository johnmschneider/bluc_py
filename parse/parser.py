from parse.token import BLUC_EOF
from parse.token import Token
from parse.result import Result
from parse.result_type import ResultType

import sys

class Parser(object):
    def __init__(self, lexedTokens):
        from parse.exprs.expr_parser import ExprParser
        from parse.stmts.stmt_parser import StmtParser

        super().__init__()

        self._lexedTokens = None

        # current token index
        self._curTokIndex = -1

        # current token
        self._curTok = Token()

        # abstract syntax tree
        self._ast = []

        self._lexedTokens = lexedTokens
        self._exprParser = ExprParser(self)
        self._stmtParser = StmtParser(self)

        # whether or not we encounter a "\" as the
        #   last non-whitespace token in a line
        self._isMultilineStmt = False

        # initialize first token
        self.setCurTok(self._curTokIndex)

    def peek(self, offset):
        endIndex = len(self._lexedTokens) - 1

        if self._curTokIndex + offset < 0:
            # start of file token
            return self._lexedTokens[0]

        elif self._curTokIndex + offset > endIndex:
            # end of file token
            return self._lexedTokens[endIndex]

        return self._lexedTokens[self._curTokIndex + offset]

    def peekMatches(self, arg1, arg2 = None):
        thingsToMatch = arg1
        peekOffset = 1

        if arg2 != None:
            peekOffset = arg2

        if (isinstance(arg1, list)):
            return self.peek(peekOffset).matchesAny(thingsToMatch)
        elif(isinstance(arg1, str)):
            return self.peek(peekOffset).matches(thingsToMatch)

    # returns if the current token matches anything in the list/str thingsToMatch
    def curTokMatches(self, thingsToMatch) -> bool:
        return self.peekMatches(thingsToMatch, 0)

    def curLineNumber(self) -> int:
        return self._curTok.lineNum

    def curColNumber(self) -> int:
        return self._curTok.column

    # sets both the current index and current token to the index at index
    def setCurTok(self, index):
        endIndex = len(self._lexedTokens) - 1
        startLineNum = self._curTok.lineNum

        if index < 0:
            # start of file token
            self._curTokIndex = 0
            self._curTok = self._lexedTokens[0]

        elif index > endIndex:
            # end of file token
            self._curTokIndex = endIndex
            self._curTok = self._lexedTokens[endIndex]

        else:
            self._curTokIndex = index
            self._curTok = self._lexedTokens[index]

        if self._curTok.lineNum != startLineNum:
            # reset our multiline stmt flag as we are on
            #   a different line now
            self._isMultilineStmt = False

    def getCurIndex(self):
        return self._curTokIndex

    def tokenAt(self, index):
        endIndex = len(self._lexedTokens) - 1

        if index < 0:
            # start of file token
            return self._lexedTokens[0]

        elif index > endIndex:
            # end of file token
            return self._lexedTokens[endIndex]

        else:
            return self._lexedTokens[index]

    # *just* moves to the next token, doesn't does
    #   perform any multiline checks, etc.
    #
    # used by the nextTok function to avoid infinite
    #   recursion
    def _rawNextTok(self):
        self.setCurTok(self._curTokIndex + 1)

    def nextTok(self) -> Result:
        outcome = Result()

        self.setCurTok(self._curTokIndex + 1)

        if self._isMultilineStmt:
            if not isspace(self.curTokText()):
                outcome.setError(self.curTok(), 
                    "Expected nothing or whitespace " +
                    "after multi-line specifier, found `" +
                    self.curTokText() + "`")
        else:
            if (self.atEOL()):
                curIndex = self._curTokIndex
                self._rawNextTok()

                # calculate if the next line is a multiline statement
                #
                #   (should work even on the first line because of the
                #   start_of_line token -- it's on line index -1)
                while not self.atEOL():
                    if self.curTokMatches(["\\"]):
                        self._isMultilineStmt = True
                        break
                    self._rawNextTok()

                self.setCurTok(curIndex)
                # TODO - finish calculating if we're on a multiline statement
        
    def curTok(self):
        return self._curTok
    
    def curTokText(self):
        return self._curTok.text

    def ast(self):
        return self._ast

    def printError(self, stmtResult : ResultType):
        # TODO - perform proper error handling
        print("[parser.printError]: Statement parsing failed on line " + str(self.curTok().lineNum), file=sys.stdout)
        print("[parser.printError]:   " + stmtResult.errCode, file=sys.stdout)

    def parse(self):
        # advance off of the "start of file" token
        self.nextTok()

        while not self.atEOF():
            stmtResult = self._stmtParser.tryParseStmt()

            if (stmtResult.successful and stmtResult.data.startLineNumber == 14):
                stopHere = 0

            if stmtResult.successful:
                self._ast.append(stmtResult.data)
            else:
                self.printError(stmtResult)

            self.nextTok()
            
        print("Parser.parse: ")
        print(self._ast)

    def atEOF(self):
        return self.curTok() == BLUC_EOF

    # check if parser is at the end of the line (i.e. if the
    #   parser is currently on the last token of this line)
    def atEOL(self):
        # these statements are separated into multiple
        #   lines so the debugger can show the values
        #   (currently, function isn't working)

        peekedTok = self.peek(1)
        curLineNum = self.curLineNumber()

        return peekedTok.lineNum != curLineNum

    def atEndOfStatement(self):
        atEnd = self._isMultilineStmt == False
        atEnd = (atEnd or self.atEOF())
        atEnd = (atEnd and self.curTokMatches(["\n", ";"]))

        return atEnd

    def isMultilineStmt(self) -> bool:
        return self._isMultilineStmt
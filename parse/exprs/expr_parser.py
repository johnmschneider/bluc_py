from parse.exprs.grouping_builder import GBuilder
from parse.token import BLUC_EOF, BLUC_SOF
from parse.result_type import ResultType
from parse.exprs.expr import *

class ExprParser(object):
    def __init__(self, parser):
        self._parser = None

        # whether or not this expression carries on to the next line
        self._isMultiline = False
        self._curLineNum = 1

        self._parser = parser


    def _checkIfMultiline(self):
        newLineNum = self._parser.curTok().lineNum

        # if we had to rewind the parser then _isMultiline will still be
        #   appropriately updated below.
        # otherwise we are on the next line.
        if newLineNum != self._curLineNum:
            self._curLineNum = newLineNum

        self._isMultiline = self._parser.peekMatches(0, "\\")

    # returns whether or not we are at a character that can never be a 
    #   continuation of an expression (such as a newline)
    def _atExprEnd(self) -> bool:
        #   commented out old code because it wasn't working
        #
        #
        # newLineNum = self._parser.curTok().lineNum
        # self._checkIfMultiline()

        # # TODO - check if this will interfere with rewinding the parser
        # if newLineNum != self._curLineNum:
        #     self._curLineNum = newLineNum
            
        #     if self._isMultiline:
        #         return False
        #     else:
        #         return True

        # return False
        
        curTokText = self._parser.curTokText()

        if self._parser.atEOL() and not self._parser.isMultilineStmt():
            return True
        else:
            # this should also apply to multiline statements
            return self._parser.curTokMatches(["{", "}", "\n"])

    def tryParseExpr(self) -> ResultType:
        result = ResultType()
        curTok = self._parser.curTok()
        
        if curTok == BLUC_EOF or curTok == BLUC_SOF:
            lit = Literal(curTok)

            result.setData(lit)
            nextResult = self._parser.nextTok()

            if (nextResult.failed()):
                result.setError(errToken, errCode)
        else:
            result = self.tryParseComma()

        return result

    def tryParseComma(self):
        # TODO - implement
        return self.tryParseAssign()

    # all assignment operators, =, ++, -=, *=, /=, %=, <<=, >>=, &=, ^=, |=
    def tryParseAssign(self):
        # TODO - implement
        return self.tryParseTernary()

    # do I even want this?
    def tryParseTernary(self):
        # TODO - implement
        return self.tryParseLogical()

    # &&, ||
    def tryParseLogical(self):
        # TODO - implement
        return self.tryParseBitwise()

    # &, ^, |
    def tryParseBitwise(self):
        # TODO - implement
        return self.tryParseEquals()

    # == and !=
    def tryParseEquals(self):
        parser = self._parser
        curOpIsEquals = False
        startIndex = parser.getCurIndex()
        result = None

        # peek ahead to see if we can match an equals
        while not parser.atEOF():
            # stop at the next line (if no multiline char is found), or
            #   tokens that can't be the right-op of the ==
            if self._atExprEnd() or \
                parser.curTokMatches([";", "{", "}"]):

                break
            elif parser.curTokMatches(["!=", "=="]):
                curOpIsEquals = True
                break

            parser.nextTok()

        parser.setCurTok(startIndex)

        if (curOpIsEquals):
            result = self.parseEquals()
        else:
            result = self.tryParseRelational()

        return result

    def parseEquals(self):
        left = self.tryParseRelational()
        right = None
        result = None
        parser = self._parser

        # parse first comparison in potential comparison chain
        if parser.curTokMatches(["!=", "=="]):
            op = parser.curTok()

            parser.nextTok()

            right = self.tryParseRelational()
            result = ResultType().setData(Binary(op, left.data, right.data))

        # handle subsequent comparisons in the chain
        while parser.curTokMatches(["!=", "=="]):
            op = parser.curTok()

            parser.nextTok()

            left = right
            right = self.tryParseRelational()
            result = ResultType().setData(Binary(op, left.data, right.data))
            
        if result == None:
            return left
        else:
            return result

    # <, <=, >, and >=
    def tryParseRelational(self):
        result = self.tryParseBitshift()
        parser = self._parser

        while parser.curTokMatches([">", ">=", "<", "<="]):
            op = parser.curTok()

            parser.nextTok()

            right = self.tryParseBitshift()

            if right.successful:
                result = ResultType().setData(Binary(op, result.data, right.data))
            else:
                # copy "right"'s error to result's error
                result.setErrFromResult(right)
                break

        return result

    def tryParseBitshift(self):
        # TODO - implement
        return self.tryParseAddSub()
    
    # try to parse add/subtract or higher
    def tryParseAddSub(self):
        result = self.tryParseMulDivMod()
        parser = self._parser

        while parser.curTokMatches(["+", "-"]):
            op = parser.curTok()
            
            parser.nextTok()

            right = self.tryParseMulDivMod()
            result = ResultType().setData(Binary(op, result.data, right.data))

        return result

    # try to parse multiple/divide/modulus or higher
    def tryParseMulDivMod(self):
        result = self.tryParseUnary()
        parser = self._parser

        while parser.curTokMatches(["/", "*"]):
            op = parser.curTok()

            parser.nextTok()
            
            right = self.tryParseUnary()
            result = ResultType().setData(Binary(op, result.data, right.data))

        return result

    # try to parse unary or higher
    def tryParseUnary(self):
        parser = self._parser

        while parser.curTokMatches(["!", "-"]):
            op = parser.curTok()

            parser.nextTok()

            right = self.tryParseUnary()
            result = ResultType().setData(Unary(op, right.data))
            return result

        return self.tryParseSizeof()

    def tryParseSizeof(self):
        # TODO - implement
        return self.tryParsePrefix()
    
    def tryParsePrefix(self):
        # TODO - implement
        return self.tryParsePostfix()

    def tryParsePostfix(self):
        result = ResultType()
        curTok = self._parser.curTok()

        result.setErrCode("ExprParser.tryParsePostFix error")

        prevTok = self._parser.peek(-1)
        if issubclass(type(prevTok), VarCall) and \
            curTok.matchesAny(["++", "--"]):

            self._parser.nextTok() # TODO - actually write this
        else:
            result = self.tryParseArrayIndex()
            
        return result

    def tryParseArrayIndex(self):
        # TODO - implement
        return self.tryParseDot()

    # object.example
    def tryParseDot(self):
        # TODO - implement
        return self.tryParseArrow()
    
    # aStructPtr->example
    def tryParseArrow(self):
        # TODO - implement
        return self.tryParseGrouping()

    def tryParseGrouping(self):
        result = ResultType()
        curTok = self._parser.curTok()

        result.setErrCode("ExprParser.tryParseGrouping: can't parse expr")

        if curTok.matches("("):
            group = None
            builder = GBuilder()
            builder.openParen = curTok

            self._parser.nextTok()
            insideExpr = self.tryParseExpr()

            if insideExpr.successful:
                builder.inside = insideExpr.data
                builder.closeParen = self._parser.curTok()
                group = builder.build()

                result.setData(group)

            # move to the next token regardless
            self._parser.nextTok()
        elif curTok.matches(")"):
            lit = Literal(curTok)

            self._parser.nextTok()
            result.setData(lit)
        else:    
            result = self.fallbackParse()

        return result
    
    # returns an invalid-parse node which will allow parser to continue but
    #   not compile
    def fallbackParse(self) -> ResultType:
        result = ResultType()
        curTok = self._parser.curTok()
        
        result.setErrCode("ExprParser.fallbackParse: invalid start of " + \
            "expression \"" + curTok.text + "\"")

        # TODO - temp test, just return literal for testing purposes
        # lit = Literal(curTok)
        # result.setData(lit)

        # consume invalid token
        self._parser.nextTok()

        return result

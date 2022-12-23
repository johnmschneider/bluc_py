from parse.token import BLUC_EOF
from parse.exprs.expr import *

class AstPrinter(object):
    def __init__(self, parser):
        self._parser = parser
        self._ast = parser.ast()

    def printToOut(self):
        print("AstPrinter.printToOut:")
        print(self.printToString())


    def printToString(self):
        output = ""

        for curNode in self._ast:
            curType = type(curNode)
            print("AstPrinter.printToOut:")
            
            # TODO - change EOF from token literal to statement so that we
            #   can just directly use == on the EOF statement here
            if issubclass(curType, Literal):
                if curNode.oper == BLUC_EOF:
                    break

            output += self._printNodeToString(curNode) + "\n"

        return output
    
    # prints a node and all of its sub-nodes to a string
    def _printNodeToString(self, node):
        output = ""
        curType = type(node)

        if issubclass(curType, Expr):
            output += self._printExpr(node, curType)

        return output

    def _printExpr(self, curTok, curType):
        output = "("

        if issubclass(curType, Binary):
            output += curTok.oper.text + " "
            output += self._printNodeToString(curTok.leftOpd) + " "
            output += self._printNodeToString(curTok.rightOpd) + ")"

        elif issubclass(curType, Unary):
            output += curTok.oper.text + " "
            output += self._printNodeToString(curTok.opd) + ")"

        elif issubclass(curType, Grouping):
            output += "grouping " + self._printNodeToString(curTok.inside) + ")"

        elif issubclass(curType, Literal):
            output += "lit " + curTok.oper.text + ")"

        elif issubclass(curType, VarCall):
            output += "var-call" + curTok.varName + ")"

        else:
            output = "(parse-error)"

        return output


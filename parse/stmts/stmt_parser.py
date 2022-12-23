from parse.result_type import ResultType
from parse.parser import Parser
from parse.exprs.expr_parser import ExprParser
from parse.stmts.var_decl import TypeSignSpecifier, VarDecl, VarRef
from parse.token import Token
from parse.stmts.stmt import Stmt
from parse.stmts.stmt_expr import StmtExpr

class StmtParser(object):
    def __init__(self, parser : Parser):
        super().__init__()

        self._parser = parser
        self._exprParser = ExprParser(parser)
        
    def tryParseStmt(self) -> Stmt:
        return self.tryParseVarDecl()

    def tryParseVarDecl(self):
        result  = ResultType()
        parser  = self._parser
        vdecl   = VarDecl()

        if (parser.curTokMatches(["var"])):
            vdecl.startLineNumber = parser.curLineNumber()

            while True:
                sign    = self.tryParseVarDeclSign()
                result  = self._parseVarDecl(sign)
                vdecl.addVar(result.data)

                if (parser.curTokMatches([",", "\\"])):
                    # this is a multi-var decl
                    parser.nextTok()
                elif (parser.atEndOfStatement()):
                    # end of var decl
                    break

        else:
            expression = self._exprParser.tryParseExpr()
            
            statement = StmtExpr()
            statement.expr = expression
            statement.startLineNumber = parser.curLineNumber()

            result.setData(statement)

        return result
    
    def tryParseVarDeclSign(self):
        result = ResultType()
        parser = self._parser
        spec : TypeSignSpecifier

        tok = parser.curTok()
        text = tok.text
    
        if (text == "unsigned"):
            spec = TypeSignSpecifier.UNSIGNED
            parser.nextTok()
        elif (text == "default"): # default var
            spec = TypeSignSpecifier.UNSPECIFIED
            parser.nextTok()
        else:
            spec = TypeSignSpecifier.SIGNED
            parser.nextTok()

        result.setData(spec)
        return result

    # for statements already validated to be a var decl
    def _parseVarDecl(self, signSpecifier : TypeSignSpecifier) -> ResultType:
        parser = self._parser
        type    : Token
        varName : Token
        var     : VarRef
        result  : ResultType = ResultType()

        # TODO - implement valid typechecker
        type = parser.curTok()
        if (type.isReservedDataTypeBase() or type.isValidName()):
            parser.nextTok()
            varName = parser.curTok()

            if (varName.isValidName()):
                # TODO - implement decl + assignment
                # e.g. "int a = 22"
                var = VarRef(signSpecifier, type, varName)
                result.setData(var)
            else:
                result.setErrToken(varName).setErrCode("Expected the name of a " + \
                "var (\"" + varName.text + "\" is not a valid identifier)")
        else:
            result.setErrToken(type).setErrCode("Expected the name of a " + \
                "type (\"" + type.text + "\" is not a valid identifier)")

        return result

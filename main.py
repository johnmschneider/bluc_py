def main():
    from parse.lexer import lex
    from parse.parser import Parser
    from parse.ast_printer import AstPrinter

    print("enter filepath to compile:")

    lexedToks = lex(input())
    output = ""

    for token in lexedToks:
        output += token.text + ", "

    print(output + "\n")

    parser = Parser(lexedToks)
    parser.parse()

    astPrinter = AstPrinter(parser)
    astPrinter.printToOut()

if __name__ == "__main__":
    main()

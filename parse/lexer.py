from parse.token import Token
from parse.token import BLUC_SOF
from parse.token import BLUC_EOF
from parse.string_helper import matchesAny
from parse import comments_remover

def appendIfNotWhitespace(lexedTokens, filepath, lineNum, column, wordSoFar):
    if wordSoFar and not wordSoFar.isspace():
        token = Token()
        token.filePath = filepath
        token.lineNum = lineNum
        token.column = column
        token.text = wordSoFar

        lexedTokens.append(token)

def lex(filepath):
    linesOfFile = comments_remover.run(filepath)
    
    lineNum = 1
    column = 1

    # whether or not to check next token for a multi-token operator like +=
    checkNextToken = False 
    lexedTokens = [BLUC_SOF]

    inString = False
    lastCharWasEscape = False

    for line in linesOfFile:
        wordSoFar = ""
    
        for char in line:
            if char == '"':
                if not inString:
                    appendIfNotWhitespace(lexedTokens, filepath, lineNum, \
                        column, wordSoFar)
                    appendIfNotWhitespace(lexedTokens, filepath, lineNum, \
                        column, '"')

                    inString = True
                    lastCharWasEscape = False
                    checkNextToken = False
                elif not lastCharWasEscape:
                    appendIfNotWhitespace(lexedTokens, filepath, lineNum, \
                        column, wordSoFar)
                    appendIfNotWhitespace(lexedTokens, filepath, lineNum, \
                        column, '"')

                    inString = False
                    wordSoFar = ""
                    checkNextToken = False
                    lastCharWasEscape = False
            else:
                lastCharWasEscape = False

                if inString:
                    if inString and char == '\\':
                        lastCharWasEscape = True
                    else:
                        wordSoFar += char

                else:        
                    if char.isspace():
                        appendIfNotWhitespace(lexedTokens, filepath, lineNum, \
                            column, wordSoFar)

                        wordSoFar = ""
                        checkNextToken = False
                    elif matchesAny(char, ['(', ')', '{', '}', '[', ']']):

                        appendIfNotWhitespace(lexedTokens, filepath, lineNum, \
                            column, wordSoFar)
                        appendIfNotWhitespace(lexedTokens, filepath, lineNum, \
                            column, char)

                        wordSoFar = ""
                        checkNextToken = False
                    elif matchesAny(char, ['+', '-', '*', '/', '%', '=', '!', \
                        '<', ">", '|', '&', '^']):

                        if (checkNextToken):
                            wordSoFar += char
                            
                            appendIfNotWhitespace(lexedTokens, filepath, \
                                lineNum, column, wordSoFar)

                            wordSoFar = ""
                            checkNextToken = False
                        else:
                            appendIfNotWhitespace(lexedTokens, filepath, \
                                lineNum, column, wordSoFar)

                            wordSoFar = char
                            checkNextToken = True
                    else:
                        wordSoFar += char
            column += 1
        lineNum += 1
    lexedTokens.append(BLUC_EOF)
    return lexedTokens
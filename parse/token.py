from parse import keywords, string_helper

class Token(object):
    import parse.string_helper

    def __init__(self) -> None:
        super().__init__()

        self.filePath = None
        self.lineNum = -1
        self.column = -1
        self.text = "" # text of token

    def matchesAny(self, stringsToMatch):
        return string_helper.matchesAny(self.text, stringsToMatch)

    def matches(self, strToMatch):
        return self.text == strToMatch

    
    # Returns true if this token's text matches a plain-old-data 
    #   type specifier.
    def isReservedDataTypeBase(self) -> bool:
        # TODO - replace .equals with ==
        return self.matchesAny(keywords.DEFAULT_TYPES)

    def isReservedWord(self) -> bool:
        return  self.matchesAny(keywords.RESERVED_WORDS) or \
                self.isReservedDataTypeBase()
            
    
    def isReservedLexeme(self) -> bool:
        char0 : str = self.text[0]
        
        return string_helper.matchesAny(char0, keywords.RESERVED_LEXEMES)
    

     # Whether or not this token is named something that might be used as a
     #  reserved lexeme in the future.
     # 
     # This is for keywords or core types that weren't originally part of the
     #  specification but are now required in common tasks.
    def isFutureReservation(self) -> bool:
        text : str = self.text
        
        isFutureReservation : bool = \
            text[0] == '_' and text[1] == '_' and \
            text[2].isalnum() # is alpha numeric?
        
        return isFutureReservation
    
    def isValidName(self) -> bool:
        startChar : str = self.text[0]
                
        return not (self.isFutureReservation() or startChar.isdigit() or \
            self.isReservedWord() or self.isReservedLexeme())

# bluc start-of-file
BLUC_SOF = Token()
BLUC_SOF.text = "__bluc_sof"

# bluc end-of-file
BLUC_EOF = Token()
BLUC_EOF.text = "__bluc_eof"
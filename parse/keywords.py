DEFAULT_TYPES = ["bool", "char", "i8", "i16", "i32", "i64", "u8", \
    "u16", "u32", "u64", "f32", "f64"]


RESERVED_WORDS = [\
    # bluc terms
    "class", "extends", "typeof", "pack",
    
    # c terms
    "auto", "break", "case", "const", "continue", "default", "do",
    "else", "enum", "extern", "for", "goto", "if", "inline", 
    "long", "register", "restrict", "return", "short", "signed",
    "sizeof", "static", "struct", "switch", "typedef", "union",
    "unsigned", "void", "volatile", "while"]

RESERVED_LEXEMES = [\
    "(", ")", "[", "]", "{", "}", "=", ";", "+", "-", "/", "*", "%" \
    "#", ",", "<", ">", ".", "&", "|"]
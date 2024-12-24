##############
# IMPORTS
##############
import string

############## 
# CONSTANTS - From the Regular definition from docu. 
##############
UPPER_LETTERS = string.ascii_uppercase
LOWER_LETTERS = string.ascii_lowercase
ALPHA = string.ascii_letters
ZERO = '0'
DIGIT = '123456789'
NUMERIC = ZERO + DIGIT
ALPHA_NUMERIC = ALPHA + NUMERIC
PUNCTUATION_SYMBOLS = string.punctuation
ASCII = ALPHA_NUMERIC + PUNCTUATION_SYMBOLS + ' \t'
ARITH_OP = '+-*/%='
RELATION_OP = '<>!&|'
ALL_OPERATOR = ARITH_OP + RELATION_OP

keywords = [
    "domain", "expansion", "null", "int", "float", "string", "bool",
    "restrict", "invoke", "capture", "true", "false",
    "vow", "else vow", "else", "boogie", "woogie",
    "default", "cycle", "sustain", "perform",
    "dismiss", "hop", "recall", "cleave",
    "dismantle", "len", "curse"
]

# FROM THE DELIMITERS 
delim_map = {
    'adr_delim':        set(ALPHA_NUMERIC + ' '),
    'arith_delim':      set(ALPHA_NUMERIC + ' ' + '-' + '('),
    'assign_delim':     set(ALPHA_NUMERIC + ' ' + '"' + '-' + '(' + ')' + '[' + '\n'),
    'boogie_delim':     {'(', ' ', '\n', '{'},
    'bool_delim':       {')', ']', ',', ' '},
    'clsbrace_delim':   set(ALPHA_NUMERIC + '}' + '\n' + '\t' + ' ' + ';'),
    'clsparen_delim':   {'+', '-', '*', '/', '%', ')', '{', '}', ',', ']', '\n', ' ', ';', ':', '&', '|'},
    'clssquare_delim':  {'+', '-', '*', '/', '%', ' !', '=', '<', '>', ')', ',', '[', ']', '\n', ' ', ';'},
    'codeblk_delim':    {'{', ' '},
    'col_delim':        set(ALPHA + '\n' + '\t' + ' '),
    'comma_delim':      set(ALPHA_NUMERIC + '"' + "'" + '(' + '[' + '-' + ' '),
    'comp_delim':       set(ALPHA_NUMERIC + '"' + "'" + '(' + '-' + ' '),
    'default_delim':    {' ', ':'},
    'ex_delim':         {' ', ';', '\n','\t'},
    'ident_delim':      {'+', '-', '*', '/', '%', '!', '=', '<', '>', '(', ')', ',', '[', ']', '\n', ' ', ';', '&', '|'},
    'incdec_delim':     set(ALPHA_NUMERIC + ')' + ' ' + ';'),
    'kword_delim':      {' ', '\t'},
    'lend_delim':       set(ALPHA_NUMERIC + '#' + '#$' + '\n' + '\t' + ' ' + '}'),
    'logic_delim':      set(ALPHA + ' '),
    'minus_delim':      set(ALPHA_NUMERIC + '-' + '(' + ' '),
    'num_delim':        set(ARITH_OP + ' ' + ')' + ',' + ';' + ':' + ']' + '}'),
    'opnbrace_delim':   set(ALPHA_NUMERIC + '\n' + '"' + ' '),
    'opnparen_delim':   set(ALPHA_NUMERIC + '"' + "'" + '-' + '(' + ')' + '\n' + ' '),
    'opnsquare_delim':  set(ALPHA_NUMERIC + '"' + "'" + '-' + '(' + '[' + ']' + ' '),
    'plus_delim':       set(ALPHA_NUMERIC + '"' + "'" + '-' + '(' + ',' + ' '),
    'para_delim':       {'(', ' ', '\n'},
    'recall_delim':     set(ALPHA + ' ' + ';'), 
    'str_delim':        {'+', ')', ']', '\n', ',', ';', ' ', ':', '}'},
    'white_delim':      set(ASCII + ALL_OPERATOR + ' ' + '\n' + '\t' + '\0'),
    'woogie_delim':     set(NUMERIC + '(' + ' ')
}


##############
# ERRORS
##############
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f'\nFile: {self.pos_start.fn}, line {self.pos_start.ln + 1}\n'
        result += string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end) + '\n'
        return result

class LexicalError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Lexical Error', details)

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

##############
# POSITION
##############

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0
            
        return self
    
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#############
# TOKENS
#############

TT_INT      = 'INT'     # Whole Numbers '3'
TT_FLOAT    = 'FLOAT'   # Decimal Numbers '3.14'
TT_STRING   = 'STRING'  # Strings 

TT_PLUS     = 'PLUS'    # '+'
TT_MINUS    = 'MINUS'   # '-'
TT_MUL      = 'MUL'     # '*'
TT_DIV      = 'DIV'     # '/'
TT_MOD      = 'MODULO'  # '%'
TT_ASSIGN   = 'ASSIGN'  # '='

TT_EQ       = 'EQ'      # '=='  
TT_NE       = 'NE'      # '!='
TT_PLUSEQ   = 'PLUSEQ'   # '+='  
TT_MINUSEQ  = 'MINUSEQ' # '-='
TT_MULEQ    = 'MULEQ'   # '*='
TT_DIVEQ    = 'DIVEQ'   # '/='
TT_MODEQ    = 'MODEQ'   # '%='

TT_NOT      = 'NOT'     # '!'
TT_AND      = 'AND'     # '&&'
TT_OR       = 'OR'      # '||'
TT_LT       = 'LT'      # '<'
TT_GT       = 'GT'      # '>'
TT_LTE      = 'LTE'     # '<='
TT_GTE      = 'GTE'     # '>='

TT_POW      = 'POW'     # '**'
TT_UNARY    = 'UNARY'   # '++', '--'
TT_ELLIPSIS = 'ELLIPSIS'# '...'

TT_LPAREN   = 'LPAREN'  # '('
TT_RPAREN   = 'RPAREN'  # ')'
TT_LSQUARE  = 'LSQUARE' # '['
TT_RSQUARE  = 'RSQUARE' # ']'
TT_LBRACE   = 'LBRACE'  # '{'
TT_RBRACE   = 'RBRACE'  # '}'
TT_SEMICOL  = 'SEMICOL' # ';'
TT_COL      = 'COLON'   # ':'
TT_COMMA    = 'COMMA'   # ','

TT_EOF      = 'EOF'     # End of File
TT_SPACE    = 'SPACE'   # Space ' '
TT_TAB      = 'TAB'     # Newline '\n'
TT_NEWLINE  = 'NEWLINE' # Tab '\t'


TT_KEYWORD  = 'KEYWORD' # Keywords
TT_IDENTIFIER = 'IDENTIFIER' # Identifiers

class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value: return f'{self.type}: {self.value}'
        return f'{self.type}'
        
class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        
    def make_tokens(self):
        tokens = []
        states = []

        while self.current_char is not None:
            
            if self.current_char in ALPHA:
                ident_state = 240
                ident_str = ''
                ident_count = 0
                pos_start = self.pos.copy()

                if self.current_char == 'b':
                    states.append(1)
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()
                    if self.current_char == 'o':
                        states.append(2)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()
                        if self.current_char == 'o':
                            states.append(3)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()
                            if self.current_char == 'l':
                                states.append(4)
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()
                                if self.current_char in delim_map['kword_delim']:
                                    states.append(5)
                                    tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                    continue 
                                elif self.current_char not in delim_map['kword_delim'] and self.current_char in ALPHA + '_':
                                    pass
                                else:
                                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                    
                            if self.current_char == 'g':
                                states.append(6)
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()
                                if self.current_char == 'i':
                                    states.append(7)
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()
                                    if self.current_char == 'e':
                                        states.append(8)
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()
                                        if self.current_char in delim_map['boogie_delim']:
                                            states.append(9)
                                            tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                            continue
                                        elif self.current_char not in delim_map['boogie_delim'] and self.current_char in ALPHA + '_':
                                            pass
                                        else: 
                                            return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                
                
                                
                elif self.current_char == "c":
                    states.append(10)
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()
                    if self.current_char == "a":
                        states.append(11)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()
                        if self.current_char == "p":
                            states.append(12)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()
                            if self.current_char == "t":
                                states.append(13)
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "u":
                                    states.append(14)
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance() 
                                    if self.current_char == "r":
                                        states.append(15)
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char == "e":
                                            states.append(16)
                                            ident_str += self.current_char
                                            ident_count+=1
                                            self.advance() 
                                            if self.current_char in delim_map['para_delim']:
                                                states.append(17)
                                                tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                                continue 
                                            elif self.current_char not in delim_map['para_delim'] and self.current_char in ALPHA + '_':
                                                pass
                                            else:
                                                return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                    if self.current_char == "l":
                        states.append(18)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance() 
                        if self.current_char == "e":
                            states.append(19)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance() 
                            if self.current_char == "a":
                                states.append(20)
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance() 
                                if self.current_char == "v":
                                    states.append(21)
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance() 
                                    if self.current_char == "e":
                                        states.append(22)
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance() 
                                        if self.current_char in delim_map['para_delim']:
                                            states.append(23)
                                            tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                            continue
                                        elif self.current_char not in delim_map['para_delim'] and self.current_char in ALPHA + '_':
                                            pass
                                        else:
                                            return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                    if self.current_char == "u":
                        states.append(24)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance() 
                        if self.current_char == "r":
                            states.append(25)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance() 
                            if self.current_char == "s":
                                states.append(26)
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance() 
                                if self.current_char == "e":
                                    states.append(27)
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()
                                    if self.current_char in delim_map['white_delim']:
                                        states.append(28)
                                        tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos)) 
                                        continue
                                    if self.current_char not in delim_map['white_delim'] and self.current_char in ALPHA + '_':
                                        pass
                                    else:
                                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                    if self.current_char == "y":
                        states.append(29)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance() 
                        if self.current_char == "c":
                            states.append(30)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance() 
                            if self.current_char == "l":
                                states.append(31)
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance() 
                                if self.current_char == "e":    
                                    states.append(32)
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()
                                    if self.current_char in delim_map['para_delim']:
                                        states.append(33)
                                        tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                        continue 
                                    if self.current_char not in delim_map['para_delim'] and self.current_char in ALPHA + '_':
                                        pass
                                    else:
                                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                elif self.current_char == "d":
                    states.append(34)
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance() 
                    if self.current_char == "e":
                        states.append(35)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance() 
                        if self.current_char == "f":
                            states.append(36)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "a":
                                states.append(37)
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()   
                                if self.current_char == "u":
                                    states.append(38)
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "l":
                                        states.append(39)
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char == "t":
                                            states.append(40)
                                            ident_str += self.current_char
                                            ident_count+=1
                                            self.advance()  
                                            if self.current_char in delim_map['default_delim']:
                                                states.append(41)
                                                tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                                continue
                                            elif self.current_char not in delim_map['default_delim'] and self.current_char in ALPHA + '_':
                                                pass
                                            else:
                                                return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                    if self.current_char == "i":
                        states.append(42)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "s":
                            states.append(43)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "m":
                                states.append(44)
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "a":
                                    states.append(45)
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "n":
                                        states.append(46)
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char == "t":
                                            states.append(47)
                                            ident_str += self.current_char
                                            ident_count+=1
                                            self.advance()  
                                            if self.current_char == "l":
                                                states.append(48)
                                                ident_str += self.current_char
                                                ident_count+=1
                                                self.advance()  
                                                if self.current_char == "e":
                                                    states.append(49)
                                                    ident_str += self.current_char
                                                    ident_count+=1
                                                    self.advance()  
                                                    if self.current_char in delim_map['para_delim']:
                                                        states.append(50)
                                                        tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                                        continue
                                                    elif self.current_char not in delim_map['para_delim'] and self.current_char in ALPHA + '_':
                                                        pass
                                                    else:
                                                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                if self.current_char == "i":
                                    states.append(51)
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "s":
                                        states.append(52)
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char == "s":
                                            states.append(53)
                                            ident_str += self.current_char
                                            ident_count+=1
                                            self.advance()
                                            if self.current_char in delim_map['ex_delim']:
                                                states.append(54)
                                                tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                                continue
                                            elif self.current_char not in delim_map['ex_delim'] and self.current_char in ALPHA + '_':
                                                pass
                                            else:
                                                return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                    if self.current_char == "o":
                        states.append(55)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()      
                        if self.current_char == "m":
                            states.append(56)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "a":
                                states.append(57)
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "i":
                                    states.append(58)
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "n":
                                        states.append(59)
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char in delim_map['para_delim']:
                                            states.append(60)
                                            tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                            continue
                                        elif self.current_char not in delim_map['para_delim'] and self.current_char in ALPHA + '_':
                                            pass
                                        else:
                                            return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
            
                elif self.current_char == "e":
                    states.append(61)
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()  
                    if self.current_char == "l":
                        states.append(62)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "s":
                            states.append(63)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "e":
                                states.append(64)
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()
                                if self.current_char in delim_map['codeblk_delim']: 
                                    states.append(65)
                                    tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                    continue
                                elif self.current_char not in delim_map['codeblk_delim'] and self.current_char in ALPHA + '_':
                                    pass
                                else:
                                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                
                    if self.current_char == "x":
                        states.append(66)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "p":
                            states.append(67)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "a":
                                states.append(68)
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "n":
                                    states.append(69)
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "s":
                                        states.append(70)
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char == "i":
                                            states.append(71)
                                            ident_str += self.current_char
                                            ident_count+=1
                                            self.advance()  
                                            if self.current_char == "o":
                                                states.append(72)
                                                ident_str += self.current_char
                                                ident_count+=1
                                                self.advance()  
                                                if self.current_char == "n":
                                                    states.append(73)
                                                    ident_str += self.current_char
                                                    ident_count+=1
                                                    self.advance()  
                                                    if self.current_char in delim_map['ex_delim']:
                                                        states.append(74)
                                                        tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                                        continue
                                                    elif self.current_char not in delim_map['ex_delim'] and self.current_char in ALPHA + '_':
                                                        pass
                                                    else:
                                                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                
                elif self.current_char == "f":
                    states.append(75)
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance() 
                    if self.current_char == "a":
                        states.append(76)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance() 
                        if self.current_char == "l":
                            states.append(77)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance() 
                            if self.current_char == "s":
                                states.append(78)
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()    
                                if self.current_char == "e":
                                    states.append(79)
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char in delim_map['bool_delim']:
                                        states.append(80)
                                        tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                        continue
                                    elif self.current_char not in delim_map['bool_delim'] and self.current_char in ALPHA + '_':
                                        pass
                                    else:
                                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                    if self.current_char == "l":
                        states.append(81)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "o":
                            states.append(82)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "a":
                                states.append(83)
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "t":
                                    states.append(84)
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char in delim_map['kword_delim']:
                                        states.append(85)
                                        tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                        continue
                                    elif self.current_char not in delim_map['kword_delim'] and self.current_char in ALPHA + '_':
                                        pass
                                    else:
                                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")

                elif self.current_char == "h":
                    states.append(86)
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()  
                    if self.current_char == "o":
                        states.append(87)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "p":
                            states.append(88)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char in delim_map['ex_delim']: 
                                states.append(89)
                                tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                continue
                            elif self.current_char not in delim_map['ex_delim'] and self.current_char in ALPHA + '_':
                                pass
                            else:
                                return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                
                elif self.current_char == "i":
                    states.append(90)
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()  
                    if self.current_char == "n":
                        states.append(91)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "v":
                            states.append(92)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "o":
                                states.append(93)
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "k":
                                    states.append(94)
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "e":
                                        states.append(95)
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char in delim_map['para_delim']:
                                            states.append(96)
                                            tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                            continue
                                        elif self.current_char not in delim_map['para_delim'] and self.current_char in ALPHA + '_':
                                            pass
                                        else:
                                            return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                        if self.current_char == "t":
                            states.append(97)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char in delim_map['kword_delim']:
                                states.append(98)
                                tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                continue
                            elif self.current_char not in delim_map['kword_delim'] and self.current_char in ALPHA + '_':
                                pass
                            else: 
                                return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                
                elif self.current_char == "l":
                    states.append(99)
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()  
                    if self.current_char == "e":
                        states.append(100)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "n":
                            states.append(101)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char in delim_map['para_delim']:
                                tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                continue
                            elif self.current_char not in delim_map['para_delim'] and self.current_char in ALPHA + '_':
                                pass
                            else: 
                                return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")

                elif self.current_char == "n":
                    states.append(102)
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()  
                    if self.current_char == "u":
                        states.append(103)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "l":
                            states.append(104)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "l":
                                states.append(105)
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char in delim_map['white_delim']:
                                    states.append(106)
                                    tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                    continue
                                elif self.current_char not in delim_map['white_delim'] and self.current_char in ALPHA + '_':
                                    pass
                                else:
                                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                elif self.current_char == "p":
                    states.append(107)
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()  
                    if self.current_char == "e":
                        states.append(108)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "r":
                            states.append(109)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "f":
                                states.append(110)
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "o":
                                    states.append(111)
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "r":
                                        states.append(112)
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char == "m":
                                            states.append(113)
                                            ident_str += self.current_char
                                            ident_count+=1
                                            self.advance()  
                                            if self.current_char in delim_map['codeblk_delim']:
                                                states.append(114)
                                                tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                                continue
                                            elif self.current_char not in delim_map['codeblk_delim'] and self.current_char in ALPHA + '_':
                                                pass
                                            else:
                                                return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                    
                elif self.current_char == "r":
                    states.append(115)
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()  
                    if self.current_char == "e":
                        states.append(116)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "c":
                            states.append(117)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "a":
                                states.append(118)
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "l":
                                    states.append(119)
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "l":
                                        states.append(120)
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char in delim_map['recall_delim']:
                                            states.append(121)
                                            tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                            continue
                                        elif self.current_char not in delim_map['recall_delim'] and self.current_char in ALPHA + '_':
                                            pass
                                        else:
                                            return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                        if self.current_char == "s":
                            states.append(122)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "t":
                                states.append(123)
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "r":
                                    states.append(124)
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "i":
                                        states.append(125)
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char == "c":
                                            states.append(126)
                                            ident_str += self.current_char
                                            ident_count+=1
                                            self.advance()  
                                            if self.current_char == "t":
                                                states.append(127)
                                                ident_str += self.current_char
                                                ident_count+=1
                                                self.advance()  
                                                if self.current_char in delim_map['kword_delim']:
                                                    states.append(128)
                                                    tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                                    continue
                                                elif self.current_char not in delim_map['kword_delim']:
                                                    pass
                                                else:
                                                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")

                elif self.current_char == "s":
                    states.append(129)
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()  
                    if self.current_char == "t":
                        states.append(130)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "r":
                            states.append(131)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "i":
                                states.append(132)
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "n":
                                    states.append(133)
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "g":
                                        states.append(134)
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char in delim_map['kword_delim']:
                                            states.append(135)
                                            tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                            continue
                                        elif self.current_char not in delim_map['kword_delim'] and self.current_char in ALPHA + '_':
                                            pass
                                        else:
                                            return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                    if self.current_char == "u":
                        states.append(136)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "s":
                            states.append(137)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "t":
                                states.append(138)
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "a":
                                    states.append(139)
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "i":
                                        states.append(140)
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char == "n":
                                            states.append(141)
                                            ident_str += self.current_char
                                            ident_count+=1
                                            self.advance()  
                                            if self.current_char in delim_map['para_delim']:
                                                states.append(142)
                                                tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                                continue
                                            elif self.current_char not in delim_map['para_delim'] and self.current_char in ALPHA + '_':
                                                pass
                                            else:
                                                return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")

                elif self.current_char == "t":
                    states.append(143)
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()  
                    if self.current_char == "r":
                        states.append(144)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "u":
                            states.append(145)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "e":
                                states.append(146)
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char in delim_map['bool_delim']:
                                    states.append(147)
                                    tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                    continue
                                elif self.current_char not in delim_map['bool_delim'] and self.current_char in ALPHA + '_':
                                    pass
                                else:
                                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")

                elif self.current_char == "v":
                    states.append(148)
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()  
                    if self.current_char == "o":
                        states.append(149)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "w":
                            states.append(150)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char in delim_map['para_delim']:
                                states.append(151)
                                tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                continue
                            elif self.current_char not in delim_map['para_delim'] and self.current_char in ALPHA + '_':
                                pass
                            else:
                                return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")

                elif self.current_char == "w":
                    states.append(152)
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()  
                    if self.current_char == "o":
                        states.append(153)
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "o":
                            states.append(154)
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "g":
                                states.append(155)
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "i":
                                    states.append(156)
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "e":
                                        states.append(157)
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char in delim_map['woogie_delim']:
                                            states.append(158)
                                            tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                            continue
                                        elif self.current_char not in delim_map['woogie_delim'] and self.current_char in ALPHA + '_':
                                            pass
                                        else: 
                                            return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                 
                while self.current_char != None and self.current_char in ALPHA_NUMERIC + '_':
                    states.append(ident_state)
                    ident_str+=self.current_char
                    ident_count+=1
                    ident_state+=1
                    self.advance()
                ident_lower = ident_str.lower()
                if ident_lower in keywords:
                    return tokens, LexicalError(pos_start, self.pos, f"Keyword '{ident_str}' cannot be used as identifier regardless of letter-casing")
                if self.current_char not in delim_map['ident_delim']:
                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after identifier '{ident_str}'")
                if ident_count>25:
                    return tokens, LexicalError(pos_start, self.pos, "Identifier exceeded maximum character limit of 25")
                tokens.append(Token(TT_IDENTIFIER, ident_str, pos_start=pos_start, pos_end=self.pos)) 
                ident_state = 240
                continue


            elif self.current_char == '=':      # assignment operator, equals 
                states.append(159)
                tok_type = TT_ASSIGN
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    states.append(161)
                    self.advance()
                    tok_type = TT_EQ

                if tok_type == TT_ASSIGN:
                    if self.current_char not in delim_map['assign_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    else:
                        states.append(160)
                        tokens.append(Token(tok_type, '=', pos_start=self.pos))
                        continue    
                if tok_type == TT_EQ:
                    states.append(162)
                    if self.current_char not in delim_map['comp_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    else:
                        tokens.append(Token(tok_type, '==', pos_start=pos_start, pos_end=self.pos))
                        continue

            elif self.current_char == '+':          # plus, increment, plus equals
                states.append(163)
                tok_type = TT_PLUS
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '+':   
                    states.append(165)     
                    states.append
                    self.advance()
                    tok_type = TT_UNARY
                if self.current_char == '=':        
                    states.append(167)
                    self.advance()
                    tok_type = TT_PLUSEQ

                if tok_type == TT_PLUS:
                    if self.current_char not in delim_map['plus_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    else:  
                        states.append(164)
                        tokens.append(Token(tok_type, '+', pos_start=pos_start, pos_end=self.pos))
                        continue
                if tok_type == TT_UNARY:
                    if self.current_char not in delim_map['incdec_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    else:
                        states.append(166)
                        tokens.append(Token(tok_type, '++', pos_start=pos_start, pos_end=self.pos))
                        continue
                if tok_type == TT_PLUSEQ:
                    if self.current_char not in delim_map['assign_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    else:
                        states.append(168)
                        tokens.append(Token(tok_type, '+=', pos_start=pos_start, pos_end=self.pos))
                        continue
                

            elif self.current_char == '-':          # minus, decrement, minus equals
                states.append(169)
                pos_start = self.pos.copy()
                self.advance()

                if self.current_char == '-':
                    states.append(171)
                    self.advance()
                    tok_type = TT_UNARY  #  -- operator
                    if self.current_char not in delim_map['incdec_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    else:  
                        states.append(172)
                        tokens.append(Token(tok_type, '--', pos_start=pos_start, pos_end=self.pos))
                        continue

                elif self.current_char == '=':
                    states.append(173)
                    self.advance()
                    tok_type = TT_MINUSEQ  # -= operator
                    if self.current_char not in delim_map['assign_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    else: 
                        states.append(174)
                        tokens.append(Token(tok_type, '-=', pos_start=pos_start, pos_end=self.pos))
                        continue
                    
                else:
                    if len(tokens) > 0 and tokens[-1].type in [TT_INT, TT_FLOAT, TT_IDENTIFIER, TT_RPAREN]:
                        states.append(170)
                        tokens.append(Token(TT_MINUS, '-', pos_start=pos_start, pos_end=self.pos))
                    else:
                        if self.current_char in NUMERIC: 
                            tok, error = self.make_number(is_negative=True)
                            if error: return tokens, error
                            else: 
                                tokens.append(tok)
                                continue
                        else:
                            return tokens, LexicalError(pos_start, self.pos, f"Unexpected '-' without a valid number or identifier.")

        
            elif self.current_char == '*':      # multiply, power operator, multiply equals,
                states.append(175)
                tok_type = TT_MUL
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '*':
                    states.append(177)
                    self.advance()
                    tok_type = TT_POW
                if self.current_char == '=':
                    states.append(179)
                    self.advance()
                    tok_type = TT_MULEQ

                if tok_type == TT_MUL:
                    if self.current_char not in delim_map['arith_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    else:
                        states.append(176)
                        tokens.append(Token(tok_type, '*', pos_start=self.pos))
                        continue
                if tok_type == TT_POW:
                    if self.current_char not in delim_map['arith_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    else:
                        states.append(178)
                        tokens.append(Token(tok_type, '**', pos_start=pos_start, pos_end=self.pos))
                        continue
                if tok_type == TT_MULEQ:
                    if self.current_char not in delim_map['assign_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")   
                    else:
                        states.append(180)
                        tokens.append(Token(tok_type, '*=', pos_start=pos_start, pos_end=self.pos))
                        continue


            elif self.current_char == '/':      # divide, divide equals
                states.append(181)
                tok_type = TT_DIV
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    states.append(183)
                    self.advance()
                    tok_type = TT_DIVEQ

                if tok_type == TT_DIV:
                    if self.current_char not in delim_map['arith_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    else:
                        states.append(182)
                        tokens.append(Token(tok_type, '/', pos_start=self.pos))
                        continue
                if tok_type == TT_DIVEQ:
                    if self.current_char not in delim_map['assign_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    else:
                        states.append(184)
                        tokens.append(Token(tok_type, '/=', pos_start=pos_start, pos_end=self.pos))
                        continue


            elif self.current_char == '%':      # modulo, modulo equals
                states.append(185)
                tok_type = TT_MOD
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    states.append(187)
                    self.advance()
                    tok_type = TT_MODEQ

                if tok_type == TT_DIV:
                    if self.current_char not in delim_map['arith_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    else:
                        states.append(186)
                        tokens.append(Token(tok_type, '%', pos_start=self.pos))
                        continue
                if tok_type == TT_MODEQ:
                    if self.current_char not in delim_map['assign_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    else:
                        states.append(188)
                        tokens.append(Token(tok_type, '%=', pos_start=pos_start, pos_end=self.pos))
                        continue

            elif self.current_char == '!':      # not, not equals
                states.append(189)
                tok_type = TT_NOT
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    states.append(191)
                    self.advance()
                    tok_type = TT_NE

                if tok_type == TT_NOT:
                    if self.current_char not in delim_map['logic_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    else:
                        states.append(190)
                        tokens.append(Token(tok_type, '!', pos_start=self.pos))
                        continue
                if tok_type == TT_NE:
                    if self.current_char not in delim_map['assign_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    else:
                        states.append(192)
                        tokens.append(Token(tok_type, '!=', pos_start=pos_start, pos_end=self.pos))
                        continue


            elif self.current_char == '<':      # less than, less than or equal
                states.append(193)
                tok_type = TT_LT
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    states.append(195)
                    self.advance()
                    tok_type = TT_LTE

                if tok_type == TT_LT:
                    if self.current_char not in delim_map['comp_delim']:
                        states.append(194)
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    else: 
                        tokens.append(Token(tok_type, '<', pos_start=self.pos))
                        continue
                if tok_type == TT_LTE:
                    states.append(196)
                    if self.current_char not in delim_map['comp_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    else: 
                        tokens.append(Token(tok_type, '<=', pos_start=pos_start, pos_end=self.pos))
                        continue


            elif self.current_char == '>':          # greater than, greater than or equal
                states.append(197)
                tok_type = TT_GT
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    states.append(199)
                    self.advance()
                    tok_type = TT_GTE

                if tok_type == TT_GT:
                    if self.current_char not in delim_map['comp_delim']:
                        states.append(198)
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    else:
                        tokens.append(Token(tok_type, '>', pos_start=self.pos))
                        continue
                if tok_type == TT_GTE:
                    states.append(200)
                    if self.current_char not in delim_map['comp_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    else:
                        tokens.append(Token(tok_type, '>=', pos_start=pos_start, pos_end=self.pos))
                        continue



            elif self.current_char == '&':          # and operator
                states.append(201)
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '&':
                    states.append(202)
                    self.advance()
                    if self.current_char not in delim_map['logic_delim']:
                        states.append(203)
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    else:
                        tokens.append(Token(TT_AND, '&&', pos_start=pos_start, pos_end=self.pos))
                        continue
                else: return tokens, InvalidSyntaxError(pos_start, self.pos, "'&' is not a valid operator")


            elif self.current_char == '|':          # or operator
                states.append(204)
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '|':
                    states.append(205)
                    self.advance()
                    if self.current_char not in delim_map['logic_delim']:
                        states.append(206)
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    else:
                        tokens.append(Token(TT_OR, '||', pos_start=pos_start, pos_end=self.pos))
                        continue
                else: return tokens, InvalidSyntaxError(pos_start, self.pos, "'|' is not a valid operator")


            elif self.current_char == '(':          # left parenthesis
                states.append(207)
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char not in delim_map['opnparen_delim']:
                    states.append(208)
                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after parentheses")
                else:
                    tokens.append(Token(TT_LPAREN, '(', pos_start=self.pos))
                    continue


            elif self.current_char == ')':          # right parenthesis
                states.append(209)
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char not in delim_map['clsparen_delim']:
                    states.append(210)
                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after parentheses")
                else:
                    tokens.append(Token(TT_RPAREN, ')', pos_start=self.pos))
                    continue

            elif self.current_char == '[':          # left bracket
                states.append(211)
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '.':
                    states.append(213)
                    self.advance()    
                    if self.current_char == '.':
                        states.append(214)
                        self.advance()
                        if self.current_char == '.':
                            states.append(215)
                            self.advance()  
                            if self.current_char != ']':
                                states.append(216)
                                return tokens, LexicalError(pos_start, self.pos, f"Invalid clan declaration")
                            elif self.current_char == ']':
                                tokens.append(Token(TT_ELLIPSIS, '...', pos_start=self.pos))
                                continue
                if self.current_char not in delim_map['opnsquare_delim']:
                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after brackets")
                else:
                    states.append(212)
                    tokens.append(Token(TT_LSQUARE, '[', pos_start=self.pos))
                    continue


            elif self.current_char == ']':          # right bracket
                states.append(217)
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char not in delim_map['clssquare_delim']:
                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after brackets")
                else:
                    states.append(218)
                    tokens.append(Token(TT_RSQUARE, ']', pos_start=self.pos))
                    continue


            elif self.current_char == '{':          # left brace
                states.append(219)
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char not in delim_map['opnbrace_delim']:
                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after braces")
                else:
                    states.append(220)
                    tokens.append(Token(TT_LBRACE, '{', pos_start=self.pos))
                    continue


            elif self.current_char == '}':          # right brace
                states.append(221)
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char != None and self.current_char not in delim_map['clsbrace_delim']:
                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after braces")
                else:
                    states.append(222)
                    tokens.append(Token(TT_RBRACE, '}', pos_start=self.pos))
                    continue


            elif self.current_char == ',':          # comma
                states.append(223)
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char not in delim_map['comma_delim']:
                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after comma")
                else:
                    states.append(224)
                    tokens.append(Token(TT_COMMA, ',', pos_start=self.pos))
                    continue


            elif self.current_char == ':':          # colon
                states.append(225)
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char not in delim_map['col_delim']:
                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after colon")
                else:
                    states.append(226)
                    tokens.append(Token(TT_COL, ':', pos_start=self.pos))
                    continue


            elif self.current_char == ';':          # semicolon
                states.append(227)
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char != None and self.current_char not in delim_map['lend_delim']:
                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after semicolon")
                else:
                    states.append(228)
                    tokens.append(Token(TT_SEMICOL, ';', pos_start=self.pos))
                    continue
    


            elif self.current_char in NUMERIC:
                tok, error = self.make_number()     # function for making integer and float tokens
                if error: return tokens, error
                else: 
                    tokens.append(tok)
                    continue


            elif self.current_char == '"':          # function for making string
                tok, error = self.make_string()
                if error: return tokens, error      
                else: 
                    tokens.append(tok)
                    continue


            elif self.current_char == '#':          # ignore single and multi-line comments
                states.append(232)
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '$':
                    states.append(235)
                    self.advance()
                    while self.current_char in ASCII + ' ' + '\t' + '\n':
                        states.append(236)
                        self.advance()
                        if self.current_char == '$':
                            states.append(237)
                            self.advance()
                            if self.current_char == '#':
                                states.append(238)
                                break
                while self.current_char != None and self.current_char in ASCII + ' \t':
                    states.append(239)
                    self.advance()
            

            if self.current_char in ' \t\n':        # whitespace, newline, tab
                pos_start = self.pos

                # check for space
                if self.current_char == ' ':
                    states.append(294)
                    while self.current_char == ' ':
                        self.advance()
                    if self.current_char not in delim_map['white_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after space")
                    else:
                        states.append(295)
                        tokens.append(Token(TT_SPACE, ' ', pos_start=pos_start, pos_end=self.pos))
                        continue
                # check for tab
                if self.current_char == '\t':
                    states.append(296)
                    while self.current_char == '\t':
                        self.advance()
                    if self.current_char not in delim_map['white_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after tab")
                    else:
                        states.append(297)
                        tokens.append(Token(TT_TAB, '\\t', pos_start=pos_start, pos_end=self.pos))
                        continue
                # check for newline
                if self.current_char == '\n':
                    states.append(298)
                    while self.current_char == '\n':
                        self.advance()
                    if self.current_char not in delim_map['white_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after newline")
                    else:
                        states.append(299)
                        tokens.append(Token(TT_NEWLINE, '\\n', pos_start=pos_start, pos_end=self.pos))
                        continue

            else: 
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return tokens, LexicalError(pos_start, self.pos, f"Invalid Character '{char}'")
        
        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None
                

    def make_number(self, is_negative=False):  # for making numbers: int and float
        num_str = ''
        int_count = 0
        num_count = 0 
        dec_count = 0
        dot_count = 0
        pos_start = self.pos.copy()

        if is_negative:  # Prepend '-' to handle negative numbers
            num_str = '-'

        while self.current_char != None and self.current_char in NUMERIC + '.':
            if self.current_char == '.':
                self.advance()
                if self.current_char == '.':
                    pos_end = self.pos.copy()
                    return [], LexicalError(pos_start, pos_end, f"Multiple period '.' in a float assignment")
                elif self.current_char == None or self.current_char not in NUMERIC:
                    pos_end = self.pos.copy()  
                    return [], LexicalError(pos_start, pos_end, "Invalid float assignment")
                dot_count += 1
                num_str += '.'
            else:
                # checks dot count to see if num is int or float,
                # if dot count is 0, num is int, increment num_count and int_count
                # if dot count is 1, num is float and were in the least significat, increment dec_count
                if dot_count == 0:
                    num_count += 1
                    int_count +=1
                if dot_count == 1:
                    dec_count += 1

                # checks if num_count exceeds limit of 17 if number is an int
                if dot_count == 0 and num_count > 17:
                    pos_end = self.pos.copy()
                    return [], LexicalError(pos_start, pos_end, "Whole number exceeded maximum character limit of 17")
                
                # checks if num_count exceeds limit of 9 if number is a float
                if dot_count == 1 and num_count > 9:
                    pos_end = self.pos.copy()
                    return [], LexicalError(pos_start, pos_end, "Whole number exceeded maximum character limit of 17")
                
                # checks if dec_count exceeds limit of 7 if number is a float, if it exceeds then just ignore
                if dot_count == 1 and dec_count > 7:
                    self.advance()
                # append the latest character to the number string
                else:
                    num_str += self.current_char
                    self.advance()

        if self.current_char not in delim_map['num_delim']:
            pos_end = self.pos.copy()
            return [], LexicalError(pos_start, pos_end, f"Invalid delimiter '{self.current_char}' after number")

        if dot_count > 1:
            pos_end = self.pos.copy()
            return [], LexicalError(pos_start, pos_end, f"Multiple period '.' in a float assignment")
        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos), None
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos), None
        
    def make_string(self):
        id_str = ''
        pos_start = self.pos.copy()
        self.advance()

        while self.current_char != None and self.current_char in ASCII:
            if self.current_char == '"':
                self.advance() 
                if self.current_char not in delim_map['str_delim']:
                    return [], LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after string '{id_str}'")
                return Token(TT_STRING, id_str, pos_start, self.pos), None
            id_str += self.current_char
            self.advance()

        return [], InvalidSyntaxError(pos_start, self.pos, 'String not properly closed with double quotes (")')

def string_with_arrows(text, pos_start, pos_end):
    result = ''

    # Calculate indices
    idx_start = max(text.rfind('\n', 0, pos_start.idx), 0)
    idx_end = text.find('\n', idx_start + 1)
    if idx_end < 0: idx_end = len(text)

    # Generate each line
    line_count = pos_end.ln - pos_start.ln + 1
    for i in range(line_count):
        # Calculate line columns
        line = text[idx_start:idx_end]
        col_start = pos_start.col if i == 0 else 0
        col_end = pos_end.col if i == line_count - 1 else len(line) - 1

        # Append to result
        result += line + '\n' 
        result += ' ' * col_start + '^' * (col_end - col_start)

        # Re-calculate indices
        idx_start = idx_end
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0 : idx_end = len(text)

    return result.replace('\t', '')

def run(text, fn='<stdin>'):
        lexer = Lexer(fn, text)
        tokens, error = lexer.make_tokens()
        return tokens, error
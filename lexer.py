import ply.lex as lex

# List of token names.   This is always required
tokens = [
   'EQ',
   'NEQ',
   'GT',
   'GE',
   'LT',
   'LE',
   'ID',
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'MODULO',
   'LPAREN',
   'RPAREN',
   'LBRACE',
   'RBRACE',
   'LBRACKET',
   'RBRACKET',
   'ASSIGN',
   'SEMICOL',
   'COMMA',
   'STRING',
]



# Reserved words

reserved = {
    # logical operators
   'ou' : 'AND',
   'aw' : 'OR',
    # Conditions 
   'ila' : 'IF',
   'awla ila' : 'ELIF',
   'awla' : 'ELSE',
    # Loops
   'ma7ed' : 'WHILE',
   'likol' : 'FOR',
    # Boolean values
   'La' : 'False',
   'Ah' : 'True',
   # Return
   'reje3' : 'RETURN',
   # break / continue
   '5roj' : 'BREAK',
   'kmel' : 'CONTINUE',
   # output / input
   'kteb' : 'PRINT',
   '9ra'  : 'INPUT',
   # define a function
   'dala' : 'FUNCTION'
}

tokens += list(reserved.values())

# Regular expression rules for simple tokens
t_EQ       = r'=='
t_NEQ      = r'!='
t_GE       = r'>='
t_LE       = r'<='
t_LT       = r'<'
t_GT       = r'>'
t_PLUS     = r'\+'
t_MINUS    = r'-'
t_TIMES    = r'\*'
t_DIVIDE   = r'/'
t_MODULO   = r'%'
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_LBRACE   = r'{'
t_RBRACE   = r'}'
t_LBRACKET = r'\['
t_RBRACKET = r']'
t_ASSIGN   = r'='
t_SEMICOL  = r';'
t_COMMA  = r','

# regular expression for identifiers

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# A regular expression rule with some action code
def t_NUMBER(t):
    r'[+-]?[0-9]+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:len(t.value) - 1]
    return t

#comment
def t_COMMENT(t):
    r'//.*'
    pass
    # No return value. Token discarded



# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'


# Error handling rule
def t_error(t):
    print("illegal character ",t.value[0]," at line number ",t.lineno," at column number ",t.lexpos)
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test it out
data = '''
a = Ah ou Ah
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)
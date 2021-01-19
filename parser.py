import ply.yacc as yacc

# Get token from lexer

from lexer import tokens

def p_statement(p):
    '''statement : assignement
                 | expression
                 | output'''
    p[0] = p[1]

def p_assignement(p):
    'assignement : ID ASSIGN expstr'
    p[0] = p[3]

def p_output(p):
    'output : PRINT LPAREN expstr RPAREN'
    p[0] = p[3]
        
def p_exp_str(p):
    '''expstr : expression
              | ID
              | STRING'''
    p[0] = p[1]

def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-' :
        p[0] = p[1] - p[3]

def p_expression_term(p) :
    'expression : term'
    p[0] = p[1]

def p_term(p):
    '''term : term TIMES factor 
            | term DIVIDE factor 
            | term MODULO factor'''
    if p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '%':
        p[0] = p[1] % p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_expression(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_factor_number(p):
    'factor : NUMBER'
    p[0] = p[1]




# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)
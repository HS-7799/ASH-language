import ply.yacc as yacc

# Get token from lexer

from lexer import tokens




def p_instruction(p):
    '''instruction : assignement
                   | output
                   | expression
                   | condition'''
    p[0] = p[1]

def p_condition(p):
    '''condition : conditionIF
                 | conditionIFELIF
                 | conditionIFELSE'''
    p[0] = p[1]

def p_condition_if(p):
    'conditionIF : IF LPAREN expression RPAREN LBRACE instruction RBRACE'
    if p[3]:
        p[0] = p[6]
def p_condition_if_elif(p):
    '''conditionIFELIF : IF LPAREN expression RPAREN LBRACE instruction RBRACE ELSE conditionIF
                       | IF LPAREN expression RPAREN LBRACE instruction RBRACE ELSE conditionIFELSE'''
    if p[3]:
        p[0] = p[6]
    else:
        p[0] = p[9]

def p_condition_if_else(p):
    'conditionIFELSE : IF LPAREN expression RPAREN LBRACE instruction RBRACE ELSE LBRACE instruction RBRACE'
    if p[3]:
        p[0] = p[6]
    else:
        p[0] = p[10]


def p_assignement(p):
    'assignement : ID ASSIGN expString'
    p[0] = p[3]

def p_output(p):
    'output : PRINT LPAREN expString RPAREN'
    p[0] = p[3]

def p_expression_string(p):
    '''expString : expression
                 | STRING'''
    p[0] = p[1]


def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | expression EQ term
                  | expression NEQ term
                  | expression GT term
                  | expression GE term
                  | expression LT term
                  | expression LE term'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-' :
        p[0] = p[1] - p[3]
    elif p[2] == '==':
        p[0] = p[1] == p[3]
    elif p[2] == '!=':
        p[0] = p[1] != p[3]
    elif p[2] == '>' :
        p[0] = p[1] > p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]
    

def p_expression_term(p) :
    'expression : term'
    p[0] = p[1]

def p_term(p):
    '''term : term TIMES factor 
            | term DIVIDE factor 
            | term MODULO factor
            | term AND factor'''
    if p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        if p[3] != 0:
            p[0] = p[1] / p[3]
        else:
            print('Zero division error')
    elif p[2] == '%':
        p[0] = p[1] % p[3]
    

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_expression(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_factor_number_ID(p):
    '''factor : NUMBER
              | True
              | False'''
    if p[1] == 'La':
        p[0] = False
    elif p[1] == 'Ah':
        p[0] = True
    else:
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
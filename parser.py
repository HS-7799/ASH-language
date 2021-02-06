import ply.yacc as yacc
import sys
import pprint

# Get token from lexer
from lexer import tokens

# dictionnary that hold identifiers and their values
identifiers = {}

def p_program(p):
    'program : statements'
    p[0] = p[1]

def p_statements(p):
    ''' statements : statements statement
                   | statement
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_instruction(p):
    '''statement   : assignement
                   | output
                   | loop
                   | condition'''
    p[0] = p[1]

def p_loop(p):
    '''loop : FORlOOP'''
    p[0] = p[1]

def p_for_loop(p):
    'FORlOOP : FOR LPAREN ID ASSIGN expression TO expression RPAREN LBRACE statements RBRACE'
    # check if there is already a variable with the same identifier
    tmp = None
    if p[3] in identifiers:
        tmp = identifiers[p[3]]

    identifiers[p[3]] = int(p[5])
    results = []
    while identifiers[p[3]] < int(p[7]):
        results.append(p[10][0])
        identifiers[p[3]] = identifiers[p[3]] + 1
    for r in results:
        print(r)
    p[0] = p[10]

    if tmp != None:
        identifiers[p[3]] = tmp
    


# conditions
def p_condition(p):
    '''condition : conditionIF
                 | conditionIFELIF
                 | conditionIFELSE'''
    p[0] = p[1]
def p_condition_if(p):
    'conditionIF : IF LPAREN expression RPAREN LBRACE statements RBRACE'
    if p[3]:
        p[0] = p[6]
def p_condition_if_elif(p):
    '''conditionIFELIF : IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE conditionIF
                       | IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE conditionIFELSE'''
    if p[3]:
        p[0] = p[6]
    else:
        p[0] = p[9]
def p_condition_if_else(p):
    'conditionIFELSE : IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE'
    if p[3]:
        p[0] = p[6]
    else:
        p[0] = p[10]



def p_assignement(p):
    'assignement : ID ASSIGN expString SEMICOL'
    p[0] = p[3]
    value_to_assign = p[3]
    identifiers[p[1]] = value_to_assign
def p_output(p):
    'output : PRINT LPAREN expString RPAREN SEMICOL'
    print(p[3])
    p[0] = p[3]

def p_expression_string(p):
    '''expString : expression
                 | STRING'''
    p[0] = p[1]


def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]

def p_expression_comparaison(p):
    'expression : comparaison'
    p[0] = p[1]

def p_comparaison(p):
    '''comparaison : expression EQ term
                   | expression NEQ term
                   | expression GT term
                   | expression GE term
                   | expression LT term
                   | expression LE term'''

    if p[2] == '==':
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
            print("Can't divide by 0")
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
              | AccessIdentifier
              | True
              | False'''
    if p[1] == 'La':
        p[0] = False
    elif p[1] == 'Ah':
        p[0] = True
    else:
        p[0] = p[1]

def p_number(p):
    '''NUMBER : INT
              | FLOAT'''
    p[0] = p[1]

def p_access_iden(p):
    'AccessIdentifier : ID'
    p[0] = identifiers[p[1]]


# Error rule for syntax errors
def p_error(p):
    if p == None:
        token = "end of file"
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"

    print(f"Syntax error: Unexpected {token}")

start = 'program'

filename = sys.argv[1]

# Build the parser
parser = yacc.yacc()

pp = pprint.PrettyPrinter(indent=4)

with open(filename, 'r') as f:
    input = f.read()
    pp.pprint(parser.parse(input))
import ply.yacc as yacc
import sys
from helpers import flatten,display_result,for_loop,while_loop,parse_input

# Get token from lexer
from lexer import tokens


#result to display
results_display = []

#result of parsing input
results_parsed = []

# dictionnary that holds identifiers and their values
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
                   | expression
                   | loop
                   | condition'''
    p[0] = p[1]

#loop
def p_loop(p):
    '''loop : FORlOOP
            | WHILELOOP'''
    p[0] = p[1]

def p_for_loop(p):
    'FORlOOP : FOR LPAREN ID ASSIGN NUMBER TO expression RPAREN LBRACEL statements RBRACEL'
    pass
    
def p_while_loop(p):
    'WHILELOOP : WHILE LPAREN comparaison RPAREN LBRACEM statements RBRACEM'
    pass
#end loop

# conditions
def p_condition(p):
    '''condition : conditionIF
                 | conditionIFELIF
                 | conditionIFELSE'''
    p[0] = p[1]

def p_condition_if(p):
    'conditionIF : IF LPAREN expression RPAREN LBRACE statements RBRACE'
    if p[3] == 's7i7a':
        p[0] = p[6]

def p_condition_if_elif(p):
    '''conditionIFELIF : IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE conditionIF
                       | IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE conditionIFELSE'''
    if p[3] == 's7i7a':
        p[0] = p[6]
    else:
        p[0] = p[9]

def p_condition_if_else(p):
    'conditionIFELSE : IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE'
    if p[3] == 's7i7a':
        p[0] = p[6]
    else:
        p[0] = p[10]

#end conditions

#array
def p_array(p):
    'array : LBRACKET numbers RBRACKET'
    p[0] = p[2]

def p_numbers(p):
    '''
        numbers : numbers COMMA NUMBER
                | NUMBER
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]
#end array

#input
def p_input(p):
    '''input : INPUT LPAREN STRING RPAREN
             | INPUT_NUMBER LPAREN STRING RPAREN'''
    a = input(p[3])
    if p[1] == 'de5el' and type(a) is str:
        p[0] = a
    elif p[1] == 'de5elra9m':
            p[0] = float(a)
#end input

def p_var(p):
    '''
        var : ID
            | array_var
    '''
    p[0] = p[1]
    
def p_array_var(p):
    'array_var : ID LBRACKET index RBRACKET'
    value_between_brackets = p[3]
    if type(p[3]) is str:
        value_between_brackets = int(identifiers[p[3]])
    p[0] = p[1] + "[" + str(value_between_brackets) + "]"

def p_index(p):
    '''
        index : INT
              | var
    '''
    p[0] = p[1]

def p_assignement(p):
    'assignement : var ASSIGN assignedValue SEMICOL'
    if type(p[3]) is list:
        for i in range(len(p[3])):
            id = p[1] + "[" + str(i) + "]"
            identifiers[id] = p[3][i]
    identifiers[p[1]] = p[3]

def p_output(p):
    'output : PRINT LPAREN expString RPAREN SEMICOL'
    p[0] = p[3]
    results_display.append(p[3])

def p_expression_string_input(p):
    '''assignedValue : expString
                     | array
                     | input'''
    p[0] = p[1]

def p_expression_string(p):
    '''expString : expression
                 | STRING'''
    p[0] = p[1]



def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | expression OR expression
                  | expression AND expression'''
    if p[1] == 's7i7a':
        p[1] = 1
    elif p[1] == 'ghalta':
        p[1] = 0

    if p[3] == 's7i7a':
        p[3] = 1
    elif p[3] == 'ghalta':
        p[3] = 0

    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == 'ou':
        p[0] =  's7i7a' if p[1] and p[3] == 1 else 'ghalta'
    elif p[2] == 'aw':
        p[0] = 's7i7a' if p[1] or p[3] == 1 else 'ghalta'



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
        p[0] = 's7i7a' if p[1] == p[3] else 'ghalta'
    elif p[2] == '!=':
        p[0] = 's7i7a' if p[1] != p[3] else 'ghalta'
    elif p[2] == '>' :
        p[0] = 's7i7a' if p[1] > p[3] else 'ghalta'
    elif p[2] == '>=':
        p[0] = 's7i7a' if p[1] >= p[3] else 'ghalta'
    elif p[2] == '<':
        p[0] = 's7i7a' if p[1] < p[3] else 'ghalta'
    elif p[2] == '<=':
        p[0] = 's7i7a' if p[1] <= p[3] else 'ghalta'
    

def p_expression_term(p) :
    'expression : term'
    p[0] = p[1]

def p_term(p):
    '''term : term TIMES factor 
            | term DIVIDE factor 
            | term MODULO factor
    '''

    if p[1] == 's7i7a':
        p[1] = 1
    elif p[1] == 'ghalta':
        p[1] = 0

    if p[3] == 's7i7a':
        p[3] = 1
    elif p[3] == 'ghalta':
        p[3] = 0
    
    if p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[3] != 0:
        if p[2] == '/':
            p[0] = p[1] / p[3]
        elif p[2] == '%':
            p[0] = p[1] % p[3]
    else:
            print("Can't divide by 0")
    

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
    if p[1] == 'ghalta':
        p[0] = 'ghalta'
    elif p[1] == 's7i7a':
        p[0] = 's7i7a'
    else:
        p[0] = p[1]

# number = int or float
def p_number(p):
    '''NUMBER : INT
              | FLOAT'''
    p[0] = p[1]

def p_access_iden(p):
    'AccessIdentifier : var'
    try:
        p[0] = identifiers[p[1]]
    except:
        print("No such variable called",p[1])
        exit()

# Error rule for syntax errors
def p_error(p):
    if p == None:
        token = "end of file"
    else:
        token = f"{p.type}({p.value}) on line {p.lineno}"
    print(f"Syntax error: Unexpected {token}")

start = 'program'

parser = yacc.yacc()
filename = sys.argv[1]
file_handle = open(filename,"r")
# file contents is the code written in your program
file_contents = file_handle.read()

blocks = parse_input(file_contents)

for i in range(len(blocks)):
    if 'likol' in blocks[i]:
        loop = for_loop(blocks[i])
        try:
            to = int(loop["to"])
        except:
            if loop["to"] in identifiers:
                to = identifiers[loop["to"]]
            else:
                print("No such variable",loop["to"])
                exit()
        identifiers[loop["identifier"]] = int(loop["from"])
        while identifiers[loop["identifier"]] <= to:
            results_parsed.append(parser.parse(loop["statements"]))
            identifiers[loop["identifier"]] += int(loop["step"])
        del identifiers[loop["identifier"]]

    elif 'ma7ed' in blocks[i]:
        condition = while_loop(blocks[i])["condition"]
        statements = while_loop(blocks[i])["statements"]
        while True:
            if parser.parse(condition)[0] == 'ghalta':
                break
            results_parsed.append(parser.parse(statements))
    else:
        results_parsed.append(parser.parse(blocks[i]))

display_result(results_display,flatten(results_parsed))

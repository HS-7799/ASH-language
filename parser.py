import ply.yacc as yacc
import sys
from helpers import flatten,display_result,for_loops_statements,while_loops_statements

# Get token from lexer
from lexer import tokens

#function that parse a string and display the result
def parse_display(s):
    # parse s
    result = parser.parse(s)
    # add result of parsing to the array that holds results of parsing
    results_parsed.append(result)


#result to display
results_display = []

#result of parsing input
results_parsed = []

# dictionnary that holds identifiers and their values
identifiers = {}

# code that is not executed yet
content_not_executed_yet = ""

#                          ____________________________________
#                         |                                   |
# array that contains statements inside for(likom) loop {l statements }l
for_loops = []
parsed_for_loop_count = 0

#                           __________________________________________________
#                           |        ________________________________________|________________
#                           |        |                                       |              |
# array that contains (condition,statements) inside for(likom) loop ma7ed(condition){m statements }m
while_loops = []
parsed_while_loop_count = 0

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

def p_loop(p):
    '''loop : FORlOOP
            | WHILELOOP'''
    p[0] = p[1]

def p_for_loop(p):
    'FORlOOP : FOR LPAREN ID TO expression RPAREN LBRACEL statements RBRACEL'
    global identifiers
    global parsed_for_loop_count
    while identifiers[p[3]] <= int(p[5]):
        parse_display(for_loops[parsed_for_loop_count])
        identifiers[p[3]] = identifiers[p[3]] + 1
    x = "{l" + for_loops[parsed_for_loop_count] + "}l"
    parsed_for_loop_count +=  1
    content_not_executed_yet=file_contents.split(x)[1].replace('\n','')
    if  content_not_executed_yet != "":
        parse_display(content_not_executed_yet)
    

def p_while_loop(p):
    'WHILELOOP : WHILE LPAREN comparaison RPAREN LBRACEM statements RBRACEM'
    
    global parsed_while_loop_count
    while True:
        condition = parser.parse(while_loops[parsed_while_loop_count]["condition"])
        if condition[0] == 'ghalta':
            break
        parse_display(while_loops[parsed_while_loop_count]["statements"])
    x = "{m" + while_loops[parsed_while_loop_count]["statements"] + "}m"
    content_not_executed_yet=file_contents.split(x)[1].replace('\n','')
    parsed_while_loop_count +=  1
    if content_not_executed_yet != "":
        parse_display(content_not_executed_yet)
    

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


def p_assignement(p):
    'assignement : ID ASSIGN expStringInput SEMICOL'
    p[0] = p[3]
    value_to_assign = p[3]
    identifiers[p[1]] = value_to_assign
def p_output(p):
    'output : PRINT LPAREN expString RPAREN SEMICOL'
    p[0] = p[3]
    results_display.append(p[3])

def p_expression_string_input(p):
    '''expStringInput : expString
                      | input'''
    p[0] = p[1]

def p_expression_string(p):
    '''expString : expression
                 | STRING'''
    p[0] = p[1]

def p_input(p):
    '''input : INPUT LPAREN STRING RPAREN
             | INPUT_NUMBER LPAREN STRING RPAREN'''
    a = input(p[3])
    if p[1] == 'de5el' and type(a) is str:
        p[0] = a
    elif p[1] == 'de5elra9m':
            p[0] = float(a)

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

parser = yacc.yacc()
filename = sys.argv[1]
file_handle = open(filename,"r")
# file contents is the code written in your program
file_contents = file_handle.read()

# if there is any for loop(likol), i append the statement inside in for_loops array
for_loops = for_loops_statements(file_contents)

# if there is any for while(ma7ed), i append the condition,statement inside in while_loops array
while_loops = while_loops_statements(file_contents)

# parse the content of file
parser.parse(file_contents)

# display result of program
display_result(results_display,results_parsed)
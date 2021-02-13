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

def get_variable(key):
    var_name = key.split('[')[0]
    if var_name in identifiers:
        if '[' in key and ']' in key:
            if type(identifiers[var_name]) is list:
                index = int(key.split('[')[1].replace(']',''))
                if index in range(len(identifiers[var_name])):
                    return identifiers[var_name][index]
                else:
                    print("list index out of range")
                    exit()
            else:
                print("'",var_name,"' object is not subscriptable")
                exit()
        else:
            return identifiers[key]

    else:
        print("variable '",var_name,"' is not defined")

def set_variable(name,content):

    if "[" in name and "]" in name:
        array_name = name.split('[')[0]
        index = int(name.split('[')[1].replace(']',''))
        if array_name in identifiers:
            identifiers[array_name][index] = content
        else:
            print(array_name + " it's undefined")
            exit()
    else:
        identifiers[name] = content

def remove_variable(name):
    del identifiers[name]

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
                   | input
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
    '''input : INPUT LPAREN var COMMA STRING RPAREN SEMICOL
             |  INPUT_NUMBER LPAREN var COMMA STRING RPAREN SEMICOL'''
    a = input(p[5])
    if p[1] == 'de5elra9m':
        try:
            a = float(a)
        except:
            print("could not convert string to float: '" + a +"'")
            exit()
    set_variable(p[3],a)
    p[0] = a
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
        value_between_brackets = int(get_variable(p[3]))

    p[0] = p[1] + "[" + str(value_between_brackets) + "]"

def p_index(p):
    '''
        index : INT
              | var
    '''
    p[0] = p[1]

def p_assignement(p):
    'assignement : var ASSIGN assignedValue SEMICOL'
    set_variable(p[1],p[3])


def p_output(p):
    'output : PRINT LPAREN expString RPAREN SEMICOL'
    p[0] = p[3]
    results_display.append(p[3])

def p_expression_string_input(p):
    '''assignedValue : expString
                     | array'''
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
    p[0] = get_variable(p[1])

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
                to = get_variable(loop["to"])
            else:
                print("No such variable",loop["to"])
                exit()
        set_variable(loop["identifier"],int(loop["from"]))
        while get_variable(loop["identifier"]) <= to:
            results_parsed.append(parser.parse(loop["statements"]))
            value = get_variable(loop["identifier"]) + int(loop["step"])
            set_variable(loop["identifier"],value)
        remove_variable(loop["identifier"])

    elif 'ma7ed' in blocks[i]:
        condition = while_loop(blocks[i])["condition"]
        statements = while_loop(blocks[i])["statements"]
        while True:
            if parser.parse(condition)[0] == 'ghalta':
                break
            results_parsed.append(parser.parse(statements))
    
    elif 'de5el' in blocks[i]:
        if len(results_display) != 0:
            display_result(results_display,flatten(results_parsed))
            results_display = []
        results_parsed.append(parser.parse(blocks[i]))

    else:
        results_parsed.append(parser.parse(blocks[i]))

display_result(results_display,flatten(results_parsed))

print(identifiers)
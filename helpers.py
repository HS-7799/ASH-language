def for_loops_statements(s):
    statements = []
    a = s.split("{l")
    for i in range(1,len(a)):
        statements.append(str(a[i].split("}l")[0]))
    return statements

def while_loops_statements(s):
    whiles = []
    condition = ""
    b = s.split("{m")
    for i in range(1,len(b)):
        loop = {}
        if b[i-1].find("ma7ed") != -1:
            condition = b[i-1].split("(")[len(b[i-1].split("(")) - 1].split(")")[0]
        statements = b[i].split("}m")[0]
        
        loop["condition"] = condition
        loop["statements"] = statements
        whiles.append(loop)
    return whiles

def flatten(list_of_lists):
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], list):
        return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
    return list_of_lists[:1] + flatten(list_of_lists[1:])

def display_result(results_display,results_parsed):
    for i in range(len(results_display)):
        if (len(list(filter (lambda x : x == results_display[i], flatten(results_parsed)))) > 0):
            print(results_display[i])
blocks = []

def function1(s):
    block1 = s.split('{w')[0].split('ma7ed')
    while_statement = block1.pop()
    if len(block1[0]) != 0:
        if block1[0].find("de5el") != -1:
            divise_blocks(block1[0])
        else:
            blocks.append(block1[0])
    b = s.split('{w')[1].split('}w')
    blocks.append('ma7ed'+while_statement + "{w" + b[0] + "}w")
    return '}w'.join(s.split('}w')[1:])

def function2(s):
    block2 = s.split('{f')[0].split('likol')
    for_statement = block2.pop()
    if len(block2[0]) != 0:
        if block2[0].find("de5el") != -1:
            divise_blocks(block2[0])
        else:
            blocks.append(block2[0])
    b = s.split('{f')[1].split('}f')
    blocks.append('likol'+for_statement + "{f" + b[0] + "}f")
    return '}f'.join(s.split('}f')[1:])


def divise_blocks(s):
    if s.find("ma7ed") != -1 and s.find("likol") == -1 :    
        ch = function1(s)
        if len(ch) != 0:
            divise_blocks(ch)
    elif s.find("likol") != -1 and s.find("ma7ed") == -1 :
        ch = function2(s)
        if len(ch) != 0:
            divise_blocks(ch)
    elif s.find("likol") != -1 and s.find("ma7ed") != -1:
        if s.find("likol") < s.find("ma7ed"):
            ch = function2(s)
            if len(ch) != 0:
                divise_blocks(ch)
        else:
            ch = function1(s)
            if len(ch) != 0:
                divise_blocks(ch)
    # elif s.find("de5el") != -1 and s.find('{') == -1 and s.find('}') == -1 :
    #     a = s.split('de5el',1)
    #     if len(a[0]) != 0:
    #         if a[0].find("de5el") != -1 or a[0].find("likol") != -1 or a[0].find("ma7ed") != -1:
    #             divise_blocks(a[0])
    #         else:
    #             blocks.append(a[0])
    #     blocks.append("de5el" + a[1].split(');')[0] + ");")
    #     ch = ");".join(a[1].split(');')[1:])
    #     if len(ch) != 0:
    #         divise_blocks(ch)
    # this one
    # elif "{" in s and "}" in s:
    #     a = s.split('ila',1)
    #     if 'de5el' in a[0]:
    #         divise_blocks(a[0])
    #     else:
    #         blocks.append(a[0])
        
    #     if 'ila' in s and 'awla' in s:
    #         ila = 'ila'+a[1].split('}')[0] + '}'
    #         awla = 'awla'+a[1].split('awla')[1].split('}')[0]+'}'
    #         awlaila = a[1].split('}')[2:][0] + "}" 
    #         if 'de5el' in awlaila or awlaila == "}":
    #             blocks.append(ila + awla)
    #         else:
    #             blocks.append(ila + awla + awlaila)
    #     elif 'ila' in s:
    #         ila = 'ila'+a[1].split('}')[0] + '}'
    #         blocks.append(ila)
    #     ch = a[1].split('}')[len(a[1].split('}')) - 1]
    #     if len(ch) != 0:
    #         divise_blocks(ch)
    else :
        blocks.append(s)

def parse_input(s):
    return_array = []
    divise_blocks(s.replace('\n',''))
    for i in range(len(blocks)):
        if len(blocks[i]) > 0:
            return_array.append(blocks[i])

    return return_array

def for_loop(s):
    loop = {}
    a = s.split("{f")
    condition = a[0].split('(')[1].split('fi')
    loop["identifier"] = condition[0].split('=')[0].replace(' ','')
    loop["from"] = int(condition[0].split('=')[1])
    left_part = condition[1].replace(')','').replace(' ','')
    loop["to"] = left_part.split(',')[0]
    loop["step"] = left_part.split(',')[1] if len(left_part.split(',')) == 2 else 1

    for i in range(1,len(a)):
        loop["statements"] = str(a[i].split("}f")[0])
    return loop

def while_loop(s):
    condition = ""
    loop = {}
    b = s.split("{w")
    for i in range(1,len(b)):
        if b[i-1].find("ma7ed") != -1:
            condition = b[i-1].split("(")[len(b[i-1].split("(")) - 1].split(")")[0]
        statements = b[i].split("}w")[0]
        
        loop["condition"] = condition
        loop["statements"] = statements
    return loop

def flatten(list_of_lists):
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], list):
        return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
    return list_of_lists[:1] + flatten(list_of_lists[1:])

def display_result(results_display,results_parsed):
    for i in range(len(results_display)):
        if (len(list(filter (lambda x : x == results_display[i], results_parsed))) > 0) and not results_display[i] == None:
            print(results_display[i])
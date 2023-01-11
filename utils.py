#TODO: not implemented yet

def linecount(code):
    return linecount_rec(code, 0)
    

def replace(code, pattern, str_to_replace):
    new_command = []
    for command in code:
        command = command.replace(pattern, str_to_replace)
        new_command.append(command)
    return new_command

def print_code(code):
    for command in code:
        print(command)

def output_print(code):
    for command in code:
        if str(type(command))=="<class 'str'>":
            print(command)
        else:
            output_print(command)    

def linecount_rec(command, lc):
    print("lc = ", lc)
    if str(type(command))=="<class 'str'>":
        lc = lc + 1
    else:
        for com in command:
            lc = linecount_rec(com, lc)
    return lc
def double_arg_condition(command,symbol_table):
    temp_code = []

    if command[1][0]=="const":
        first_const = command[1][1]
    else:
        print(symbol_table.find_variable(command[1][1][1]))
        print(command[1][1][1])
        first_mem = symbol_table.find_variable(command[1][1][1]).get_memory_offset()

    if command[2][0]=="const":
        second_const = command[2][1]
    else:
        second_mem = symbol_table.find_variable(command[2][1]).get_memory_offset()

    if command[0]=="GT":
        # var > var
        if command[1][0]=="var" and command[2][0]=="var":
            temp_code.append("LOAD " + str(first_mem))
            temp_code.append("SUBT " + str(second_mem))
            temp_code.append("JZERO [not]")

        # var > const (uzywamy 1 komorki w pamieci)
        elif command[1][0]=="var":
            temp_code.append("SET " + str(second_const))
            temp_code.append("STORE " + str(1))
            temp_code.append("LOAD " + str(first_mem))
            temp_code.append("SUBT " + str(1))
            temp_code.append("JZERO [not]")

        # const > var
        elif command[2][0]=="var":
            temp_code.append("SET " + str(first_const))
            temp_code.append("SUBT " + str(second_mem))
            temp_code.append("JZERO [not]")

        # const > const
        else:
            if not int(first_const) > int(second_const):
                temp_code.append("JZERO [not]")
        
    elif command[0]=="LT":
        if command[1][0]=="var" and command[2][0]=="var":
            temp_code.append("LOAD " + str(second_mem))
            temp_code.append("SUBT " + str(first_mem))
            temp_code.append("JZERO [not]")

        # var > const (uzywamy 1 komorki w pamieci)
        elif command[2][0]=="var":
            temp_code.append("SET " + str(first_const))
            temp_code.append("STORE " + str(1))
            temp_code.append("LOAD " + str(second_mem))
            temp_code.append("SUBT " + str(1))
            temp_code.append("JZERO [not]")

        # const > var
        elif command[1][0]=="var":
            temp_code.append("SET " + str(second_const))
            temp_code.append("SUBT " + str(first_mem))
            temp_code.append("JZERO [not]")

        # const > const
        else:
            if not int(first_const) < int(second_const):
                temp_code.append("JZERO [not]")

    if command[0]=="LET":
        # var > var
        if command[1][0]=="var" and command[2][0]=="var":
            temp_code.append("LOAD " + str(first_mem))
            temp_code.append("SUBT " + str(second_mem))
            temp_code.append("JPOS[not]")

        # var > const (uzywamy 1 komorki w pamieci)
        elif command[1][0]=="var":
            temp_code.append("SET " + str(second_const))
            temp_code.append("STORE " + str(1))
            temp_code.append("LOAD " + str(first_mem))
            temp_code.append("SUBT " + str(1))
            temp_code.append("JPOS [not]")

        # const > var
        elif command[2][0]=="var":
            temp_code.append("SET " + str(first_const))
            temp_code.append("SUBT " + str(second_mem))
            temp_code.append("JPOS [not]")

        # const > const
        else:
            if not int(first_const) > int(second_const):
                temp_code.append("JPOS [not]")
        
    elif command[0]=="GET":
        if command[1][0]=="var" and command[2][0]=="var":
            temp_code.append("LOAD " + str(second_mem))
            temp_code.append("SUBT " + str(first_mem))
            temp_code.append("JPOS [not]")

        # var > const (uzywamy 1 komorki w pamieci)
        elif command[2][0]=="var":
            temp_code.append("SET " + str(first_const))
            temp_code.append("STORE " + str(1))
            temp_code.append("LOAD " + str(second_mem))
            temp_code.append("SUBT " + str(1))
            temp_code.append("JPOS [not]")

        # const > var
        elif command[1][0]=="var":
            temp_code.append("SET " + str(second_const))
            temp_code.append("SUBT " + str(first_mem))
            temp_code.append("JPOS [not]")

        # const > const
        else:
            if not int(first_const) < int(second_const):
                temp_code.append("JPOS [not]")
    return temp_code    

def eq_condition(command,symbol_table):
    temp_code = []

    first_const = 0
    second_const = 0
    first_mem = 0
    second_mem = 0

    if command[1][0]=="const":
        first_const = command[1][1]
    else:
        first_mem = symbol_table.find_variable(command[1][1]).get_memory_offset()

    if command[2][0]=="const":
        second_const = command[2][1]
    else:
        second_mem = symbol_table.find_variable(command[2][1]).get_memory_offset()

    if command[0]=="EQ":
        if command[1][0]=="var" and command [2][0] == "var":
            temp_code.append("LOAD " + str(first_mem))
            temp_code.append("SUBT " + str(second_mem))
            temp_code.append("JPOS [not]")
            temp_code.append("LOAD " + str(second_mem))
            temp_code.append("SUBT " + str(first_mem))
            temp_code.append("JPOS [not]")
        elif command[1][0]=="var":
            temp_code.append("SET " + str(second_const))
            temp_code.append("SUBT " + str(first_mem))
            temp_code.append("JPOS [not]")
            temp_code.append("SET " + str(second_const))
            temp_code.append("STORE " + str(1))
            temp_code.append("LOAD " + str(first_mem))
            temp_code.append("SUBT " + str(1))
            temp_code.append("JPOS [not]")
        elif command[2][0]=="var":
            temp_code.append("SET " + str(first_const))
            temp_code.append("SUBT " + str(second_mem))
            temp_code.append("JPOS [not]")
            temp_code.append("SET " + str(first_const))
            temp_code.append("STORE " + str(1))
            temp_code.append("LOAD " + str(second_mem))
            temp_code.append("SUBT " + str(1))
            temp_code.append("JPOS [not]")
        else:  
            if not int(first_const) == int(second_const):
                temp_code.append("JPOS [not]") 
    else:
        if command[1][0]=="var" and command [2][0] == "var":
            temp_code.append("LOAD " + str(first_mem))
            temp_code.append("SUBT " + str(second_mem))
            temp_code.append("JZERO [not]")
            temp_code.append("LOAD " + str(second_mem))
            temp_code.append("SUBT " + str(first_mem))
            temp_code.append("JZERO [not]")
        elif command[1][0]=="var":
            temp_code.append("SET " + str(second_const))
            temp_code.append("SUBT " + str(first_mem))
            temp_code.append("JZERO [not]")
            temp_code.append("SET " + str(second_const))
            temp_code.append("STORE " + str(1))
            temp_code.append("LOAD " + str(first_mem))
            temp_code.append("SUBT " + str(1))
            temp_code.append("JZERO [not]")
        elif command[2][0]=="var":
            temp_code.append("SET " + str(first_const))
            temp_code.append("SUBT " + str(second_mem))
            temp_code.append("JZERO [not]")
            temp_code.append("SET " + str(first_const))
            temp_code.append("STORE " + str(1))
            temp_code.append("LOAD " + str(second_mem))
            temp_code.append("SUBT " + str(1))
            temp_code.append("JZERO [not]")
        else:  
            if not int(first_const) == int(second_const):
                temp_code.append("JZERO [not]")

    return temp_code

        

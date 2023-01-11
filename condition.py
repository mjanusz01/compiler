import utils

def double_arg_condition(command,symbol_table):
    temp_code = []

    if command[1][0]=="const":
        first_const = command[1][1]
    else:
        first_mem = symbol_table.find_variable(command[1][1]).get_memory_offset()

    if command[2][0]=="const":
        second_const = command[2][1]
    else:
        print(command[2][1])
        print(symbol_table.find_variable(command[2][1]))
        second_mem = symbol_table.find_variable(command[2][1]).get_memory_offset()

    if command[0]=="GT":
        # var > var
        if command[1][0]=="var" and command[2][0]=="var":
            symbol_table.append_code(temp_code, "LOAD " + str(first_mem))
            symbol_table.append_code(temp_code, "SUBT " + str(second_mem))
            symbol_table.append_code(temp_code, "JZERO [not]")

        # var > const (uzywamy 1 komorki w pamieci)
        elif command[1][0]=="var":
            symbol_table.append_code(temp_code, "SET " + str(second_const))
            symbol_table.append_code(temp_code, "STORE " + str(1))
            symbol_table.append_code(temp_code, "LOAD " + str(first_mem))
            symbol_table.append_code(temp_code, "SUBT " + str(1))
            symbol_table.append_code(temp_code, "JZERO [not]")

        # const > var
        elif command[2][0]=="var":
            symbol_table.append_code(temp_code, "SET " + str(first_const))
            symbol_table.append_code(temp_code, "SUBT " + str(second_mem))
            symbol_table.append_code(temp_code, "JZERO [not]")

        # const > const
        else:
            if not int(first_const) > int(second_const):
                symbol_table.append_code(temp_code, "JZERO [not]")
        
    elif command[0]=="LT":
        if command[1][0]=="var" and command[2][0]=="var":
            symbol_table.append_code(temp_code, "LOAD " + str(second_mem))
            symbol_table.append_code(temp_code, "SUBT " + str(first_mem))
            symbol_table.append_code(temp_code, "JZERO [not]")

        # var > const (uzywamy 1 komorki w pamieci)
        elif command[2][0]=="var":
            symbol_table.append_code(temp_code, "SET " + str(first_const))
            symbol_table.append_code(temp_code, "STORE " + str(1))
            symbol_table.append_code(temp_code, "LOAD " + str(second_mem))
            symbol_table.append_code(temp_code, "SUBT " + str(1))
            symbol_table.append_code(temp_code, "JZERO [not]")

        # const > var
        elif command[1][0]=="var":
            symbol_table.append_code(temp_code, "SET " + str(second_const))
            symbol_table.append_code(temp_code, "SUBT " + str(first_mem))
            symbol_table.append_code(temp_code, "JZERO [not]")

        # const > const
        else:
            if not int(first_const) < int(second_const):
                symbol_table.append_code(temp_code, "JZERO [not]")

    if command[0]=="LET":
        # var > var
        if command[1][0]=="var" and command[2][0]=="var":
            symbol_table.append_code(temp_code, "LOAD " + str(first_mem))
            symbol_table.append_code(temp_code, "SUBT " + str(second_mem))
            symbol_table.append_code(temp_code, "JPOS[not]")

        # var > const (uzywamy 1 komorki w pamieci)
        elif command[1][0]=="var":
            symbol_table.append_code(temp_code, "SET " + str(second_const))
            symbol_table.append_code(temp_code, "STORE " + str(1))
            symbol_table.append_code(temp_code, "LOAD " + str(first_mem))
            symbol_table.append_code(temp_code, "SUBT " + str(1))
            symbol_table.append_code(temp_code, "JPOS [not]")

        # const > var
        elif command[2][0]=="var":
            symbol_table.append_code(temp_code, "SET " + str(first_const))
            symbol_table.append_code(temp_code, "SUBT " + str(second_mem))
            symbol_table.append_code(temp_code, "JPOS [not]")

        # const > const
        else:
            if not int(first_const) > int(second_const):
                symbol_table.append_code(temp_code, "JPOS [not]")
        
    elif command[0]=="GET":
        if command[1][0]=="var" and command[2][0]=="var":
            symbol_table.append_code(temp_code, "LOAD " + str(second_mem))
            symbol_table.append_code(temp_code, "SUBT " + str(first_mem))
            symbol_table.append_code(temp_code, "JPOS [not]")

        # var > const (uzywamy 1 komorki w pamieci)
        elif command[2][0]=="var":
            symbol_table.append_code(temp_code, "SET " + str(first_const))
            symbol_table.append_code(temp_code, "STORE " + str(1))
            symbol_table.append_code(temp_code, "LOAD " + str(second_mem))
            symbol_table.append_code(temp_code, "SUBT " + str(1))
            symbol_table.append_code(temp_code, "JPOS [not]")

        # const > var
        elif command[1][0]=="var":
            symbol_table.append_code(temp_code, "SET " + str(second_const))
            symbol_table.append_code(temp_code, "SUBT " + str(first_mem))
            symbol_table.append_code(temp_code, "JPOS [not]")

        # const > const
        else:
            if not int(first_const) < int(second_const):
                symbol_table.append_code(temp_code, "JPOS [not]")
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
            symbol_table.append_code(temp_code, "LOAD " + str(first_mem))
            symbol_table.append_code(temp_code, "SUBT " + str(second_mem))
            symbol_table.append_code(temp_code, "JPOS [not]")
            symbol_table.append_code(temp_code, "LOAD " + str(second_mem))
            symbol_table.append_code(temp_code, "SUBT " + str(first_mem))
            symbol_table.append_code(temp_code, "JPOS [not]")
        elif command[1][0]=="var":
            symbol_table.append_code(temp_code, "SET " + str(second_const))
            symbol_table.append_code(temp_code, "SUBT " + str(first_mem))
            symbol_table.append_code(temp_code, "JPOS [not]")
            symbol_table.append_code(temp_code, "SET " + str(second_const))
            symbol_table.append_code(temp_code, "STORE " + str(1))
            symbol_table.append_code(temp_code, "LOAD " + str(first_mem))
            symbol_table.append_code(temp_code, "SUBT " + str(1))
            symbol_table.append_code(temp_code, "JPOS [not]")
        elif command[2][0]=="var":
            symbol_table.append_code(temp_code, "SET " + str(first_const))
            symbol_table.append_code(temp_code, "SUBT " + str(second_mem))
            symbol_table.append_code(temp_code, "JPOS [not]")
            symbol_table.append_code(temp_code, "SET " + str(first_const))
            symbol_table.append_code(temp_code, "STORE " + str(1))
            symbol_table.append_code(temp_code, "LOAD " + str(second_mem))
            symbol_table.append_code(temp_code, "SUBT " + str(1))
            symbol_table.append_code(temp_code, "JPOS [not]")
        else:  
            if not int(first_const) == int(second_const):
                symbol_table.append_code(temp_code, "JPOS [not]") 
    else:
        if command[1][0]=="var" and command [2][0] == "var":
            symbol_table.append_code(temp_code, "LOAD " + str(first_mem))
            symbol_table.append_code(temp_code, "SUBT " + str(second_mem))
            symbol_table.append_code(temp_code, "JZERO [not]")
            symbol_table.append_code(temp_code, "LOAD " + str(second_mem))
            symbol_table.append_code(temp_code, "SUBT " + str(first_mem))
            symbol_table.append_code(temp_code, "JZERO [not]")
        elif command[1][0]=="var":
            symbol_table.append_code(temp_code, "SET " + str(second_const))
            symbol_table.append_code(temp_code, "SUBT " + str(first_mem))
            symbol_table.append_code(temp_code, "JZERO [not]")
            symbol_table.append_code(temp_code, "SET " + str(second_const))
            symbol_table.append_code(temp_code, "STORE " + str(1))
            symbol_table.append_code(temp_code, "LOAD " + str(first_mem))
            symbol_table.append_code(temp_code, "SUBT " + str(1))
            symbol_table.append_code(temp_code, "JZERO [not]")
        elif command[2][0]=="var":
            symbol_table.append_code(temp_code, "SET " + str(first_const))
            symbol_table.append_code(temp_code, "SUBT " + str(second_mem))
            symbol_table.append_code(temp_code, "JZERO [not]")
            symbol_table.append_code(temp_code, "SET " + str(first_const))
            symbol_table.append_code(temp_code, "STORE " + str(1))
            symbol_table.append_code(temp_code, "LOAD " + str(second_mem))
            symbol_table.append_code(temp_code, "SUBT " + str(1))
            symbol_table.append_code(temp_code, "JZERO [not]")
        else:  
            if not int(first_const) == int(second_const):
                symbol_table.append_code(temp_code, "JZERO [not]")

    return temp_code

        

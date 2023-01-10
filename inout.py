def write(command,symbol_table,line_count):
    temp_code = []
    if(command[1][0]=="var"):
        temp_code.append("PUT " + str(symbol_table.find_variable(command[1][1]).get_memory_offset()))
    else:
        temp_code.append("PUT " + str(command[1][1]))
    return temp_code

# TODO: implement
def read(self,command,symbol_table,line_count):
    return "Not implemented yet"

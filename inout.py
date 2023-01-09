def write(self,command,symbol_table,line_count):
    temp_code = []
    if(command[1][0]=="var"):
        self.temp_code.append("PUT ", self.symbol_table.find_variable(command[1][1]).get_memory_offset())
    else:
        self.temp_code.append("PUT ", command[1][1])

# TODO: implement
def read(self,command,symbol_table,line_count):
    return "Not implemented yet"

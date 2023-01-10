from condition import double_arg_condition, eq_condition
from code_generator import CodeGenerator
from utils import linecount, replace

def ifthen(command,symbol_table,line_count):
    
    condition_code = []
    if_code = []
    final_code = []
    line_count_start = line_count.copy()
    
    if command[1][0] == "GT" or command[1][0] == "LT" or command[1][0] == "LET" or command[1][0] == "GET":
        condition_code = double_arg_condition(command, symbol_table)
    else:
        condition_code = eq_condition(command, symbol_table)
    
    if_code = CodeGenerator.generate_code(command[2])
    
    condition_code_linecount = linecount(condition_code)
    if_code_linecount = linecount(if_code)
    
    condition_code = replace(condition_code, "[not]", str(line_count_start + condition_code_linecount + if_code_linecount))

    final_code.append(condition_code)
    final_code.append(if_code_linecount)

    return final_code

def ifelse(command,symbol_table,line_count):

    condition_code = []
    if_code = []
    else_code = []
    final_code = []
    line_count_start = line_count.copy()
    
    if command[1][0] == "GT" or command[1][0] == "LT" or command[1][0] == "LET" or command[1][0] == "GET":
        condition_code = double_arg_condition(command, symbol_table)
    else:
        condition_code = eq_condition(command, symbol_table)
    
    if_code = CodeGenerator.generate_code(command[2])
    else_code = CodeGenerator.generate_code(command[3])

    condition_code_linecount = linecount(condition_code)
    if_code_linecount = linecount(if_code)
    else_code_linecount = linecount(else_code)
    
    condition_code = replace(condition_code, "[not]", str(line_count_start + condition_code_linecount + if_code_linecount + 1))

    final_code.append(condition_code)
    final_code.append(if_code_linecount)
    final_code.append("JUMP ", str(line_count_start + condition_code_linecount + if_code_linecount + else_code_linecount + 1))
    final_code.append(else_code_linecount)

    return final_code


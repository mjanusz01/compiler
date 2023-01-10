from condition import eq_condition, double_arg_condition
from code_generator import CodeGenerator
from utils import linecount, replace

def whileloop(command,symbol_table,line_count):

    line_count_start = line_count.copy()

    if command[1][0] == "GT" or command[1][0] == "LT" or command[1][0] == "LET" or command[1][0] == "GET":
        condition_code = double_arg_condition(command, symbol_table)
    else:
        condition_code = eq_condition(command, symbol_table)

    
    inside_loop_code = CodeGenerator.generate_code(command[2])

    condition_code_linecount = linecount(condition_code)
    inside_loop_code_linecount = linecount(inside_loop_code)
    condition_code = replace(condition_code, "[not]", line_count_start+condition_code_linecount+inside_loop_code_linecount+1)
    final_code = []
    final_code.append(condition_code)
    final_code.append(inside_loop_code)
    final_code.append("JUMP ", line_count_start)
    
    return final_code

def untilloop(command, symbol_table, line_count):

    line_count_start = line_count.copy()

    if command[1][0] == "GT" or command[1][0] == "LT" or command[1][0] == "LET" or command[1][0] == "GET":
        condition_code = double_arg_condition(command, symbol_table)
    else:
        condition_code = eq_condition(command, symbol_table)

    
    inside_loop_code = CodeGenerator.generate_code(command[2])

    condition_code_linecount = linecount(condition_code)
    inside_loop_code_linecount = linecount(inside_loop_code)
    condition_code = replace(condition_code, "[not]", line_count_start+condition_code_linecount+inside_loop_code_linecount+1)

    final_code = []
    final_code.append(inside_loop_code)
    final_code.append(condition_code)
    final_code.append("JUMP ", line_count_start)

    return final_code
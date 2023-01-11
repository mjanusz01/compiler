import symbol_table
import utils
import inout
import assign
import condition

class CodeGenerator:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def generate_code(self,commands):
        print("JESTEM W GENERATORZE KOMEND!")
        code = []

        for command in commands:
            print("aktualna komenda ", command, " lc = ", self.symbol_table.get_lc())
            if command[0]=="ASSIGN":
                return_code = assign.assign(command,self.symbol_table)
                code.append(return_code)
            elif command[0]=="WRITE":
                return_code = inout.write(command,self.symbol_table)
                code.append(return_code)
            elif command[0]=="WHILE":
                return_code = whileloop(self,command, self.symbol_table)
                code.append(return_code)
            elif command[0]=="UNTIL":
                return_code = untilloop(self,command, self.symbol_table)
                code.append(return_code)
            elif command[0]=="IF":
                return_code = ifthen(self,command, self.symbol_table)
                code.append(return_code)    
            elif command[0]=="IFELSE":
                return_code = ifelse(self,command, self.symbol_table)
                code.append(return_code)
            print(code)
        utils.print_code(code)
        return code
        
def ifthen(code_generator,command,symbol_table):
        
    condition_code = []
    if_code = []
    final_code = []
    line_count_start = symbol_table.get_lc()
        
    if command[1][0] == "GT" or command[1][0] == "LT" or command[1][0] == "LET" or command[1][0] == "GET":
        print("KOMENDA", command[1])
        condition_code = condition.double_arg_condition(command[1], symbol_table)
    else:
        condition_code = condition.eq_condition(command[1], symbol_table)

    if_code = CodeGenerator.generate_code(code_generator,command[2])
    print("IFCODE ", if_code)
    condition_code_linecount = utils.linecount(condition_code)
    if_code_linecount = utils.linecount(if_code)
        
    condition_code = utils.replace(condition_code, "[not]", str(line_count_start + condition_code_linecount + if_code_linecount))
    final_code.append(condition_code)
    final_code.append(if_code)

    return final_code

def ifelse(code_generator,command,symbol_table):

    condition_code = []
    if_code = []
    else_code = []
    final_code = []
    line_count_start = symbol_table.get_lc()
        
    if command[1][0] == "GT" or command[1][0] == "LT" or command[1][0] == "LET" or command[1][0] == "GET":
        print("KOMENDA", command[1])
        condition_code = condition.double_arg_condition(command[1], symbol_table)
    else:
        condition_code = condition.eq_condition(command[1], symbol_table)
        
    if_code = CodeGenerator.generate_code(code_generator,command[2])
    else_code = CodeGenerator.generate_code(code_generator,command[3])

    condition_code_linecount = utils.linecount(condition_code)
    if_code_linecount = utils.linecount(if_code)
    else_code_linecount = utils.linecount(else_code)
    
    print("line_count_start = ", line_count_start, "condition_code_linecount = ", condition_code_linecount, "if_code_linecount = ", if_code_linecount )
    print(if_code)
    condition_code = utils.replace(condition_code, "[not]", str(line_count_start + condition_code_linecount + if_code_linecount + 1))

    final_code.append(condition_code)
    final_code.append(if_code)
    symbol_table.append_code(final_code, "JUMP " + str(line_count_start + condition_code_linecount + if_code_linecount + else_code_linecount + 1))
    final_code.append(else_code)
    
    return final_code

def whileloop(code_generator,command,symbol_table):

    line_count_start = symbol_table.get_lc()

    print("IN WHILE LOOP")
    print(command[1])
    if command[1][0] == "GT" or command[1][0] == "LT" or command[1][0] == "LET" or command[1][0] == "GET":
        condition_code = condition.double_arg_condition(command[1], symbol_table)
    else:
        condition_code = condition.eq_condition(command[1], symbol_table)
    
    inside_loop_code = CodeGenerator.generate_code(code_generator,command[2])

    condition_code_linecount = utils.linecount(condition_code)
    inside_loop_code_linecount = utils.linecount(inside_loop_code)
    condition_code = utils.replace(condition_code, "[not]", str(line_count_start+condition_code_linecount+inside_loop_code_linecount+1))
    final_code = []
    final_code.append(condition_code)
    final_code.append(inside_loop_code)
    symbol_table.append_code(final_code,"JUMP " + str(line_count_start))
        
    return final_code

def untilloop(code_generator,command, symbol_table):

    line_count_start = symbol_table.get_lc()

    print("IN WHILE LOOP")
    print(command[2])
    if command[2][0] == "GT" or command[2][0] == "LT" or command[2][0] == "LET" or command[2][0] == "GET":
        condition_code = condition.double_arg_condition(command[2], symbol_table)
    else:
        condition_code = condition.eq_condition(command[2], symbol_table)

    inside_loop_code = CodeGenerator.generate_code(code_generator,command[1])

    condition_code_linecount = utils.linecount(condition_code)
    inside_loop_code_linecount = utils.linecount(inside_loop_code)
    condition_code = utils.replace(condition_code, "[not]", str(line_count_start+condition_code_linecount+inside_loop_code_linecount+1))

    final_code = []
    final_code.append(inside_loop_code)
    final_code.append(condition_code)
    symbol_table.append_code(final_code,"JUMP " + str(line_count_start))

    return final_code
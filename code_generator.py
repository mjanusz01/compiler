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
        lc = 0
        code = []

        for command in commands:
            print("aktualna komenda ", command)
            if command[0]=="ASSIGN":
                return_code = assign.assign(command,self.symbol_table,lc)
                code.append(return_code)
            elif command[0]=="WRITE":
                return_code = inout.write(command,self.symbol_table,lc)
                code.append(return_code)
            elif command[0]=="WHILE":
                return_code = whileloop(self,command, self.symbol_table, lc)
                code.append(return_code)
            elif command[0]=="REPEAT":
                return_code = untilloop(command, self.symbol_table, lc)
                code.append(return_code)
            elif command[0]=="IF":
                return_code = ifthen(command, self.symbol_table, lc)
                code.append(return_code)    
            elif command[0]=="IFELSE":
                return_code = ifelse(command, self.symbol_table, lc)
                code.append(return_code)
            print(code)
        utils.print_code(code)
        return code
        
def ifthen(command,symbol_table,line_count):
        
        condition_code = []
        if_code = []
        final_code = []
        line_count_start = line_count
        
        if command[1][0] == "GT" or command[1][0] == "LT" or command[1][0] == "LET" or command[1][0] == "GET":
            condition_code = condition.double_arg_condition(command, symbol_table)
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
            condition_code = condition.double_arg_condition(command, symbol_table)
        else:
            condition_code = condition.eq_condition(command, symbol_table)
        
        if_code = CodeGenerator.generate_code(command[2])
        else_code = CodeGenerator.generate_code(command[3])

        condition_code_linecount = utils.linecount(condition_code)
        if_code_linecount = utils.linecount(if_code)
        else_code_linecount = utils.linecount(else_code)
        
        condition_code = utils.replace(condition_code, "[not]", str(line_count_start + condition_code_linecount + if_code_linecount + 1))

        final_code.append(condition_code)
        final_code.append(if_code_linecount)
        final_code.append("JUMP ", str(line_count_start + condition_code_linecount + if_code_linecount + else_code_linecount + 1))
        final_code.append(else_code_linecount)

        return final_code

def whileloop(code_generator,command,symbol_table,line_count):

        line_count_start = line_count

        print("IN WHILE LOOP")

        if command[1][0] == "GT" or command[1][0] == "LT" or command[1][0] == "LET" or command[1][0] == "GET":
            condition_code = condition.double_arg_condition(command, symbol_table)
        else:
            condition_code = condition.eq_condition(command, symbol_table)

        print("przekaz", command)
        inside_loop_code = CodeGenerator.generate_code(code_generator,command[2])

        condition_code_linecount = utils.linecount(condition_code)
        inside_loop_code_linecount = utils.linecount(inside_loop_code)
        condition_code = utils.replace(condition_code, "[not]", line_count_start+condition_code_linecount+inside_loop_code_linecount+1)
        final_code = []
        final_code.append(condition_code)
        final_code.append(inside_loop_code)
        final_code.append("JUMP " + str(line_count_start))
        
        return final_code

def untilloop(command, symbol_table, line_count):

        line_count_start = line_count.copy()

        if command[1][0] == "GT" or command[1][0] == "LT" or command[1][0] == "LET" or command[1][0] == "GET":
            condition_code = condition.double_arg_condition(command, symbol_table)
        else:
            condition_code = condition.eq_condition(command, symbol_table)

        
        inside_loop_code = CodeGenerator.generate_code(command[2])

        condition_code_linecount = utils.linecount(condition_code)
        inside_loop_code_linecount = utils.linecount(inside_loop_code)
        condition_code = utils.replace(condition_code, "[not]", line_count_start+condition_code_linecount+inside_loop_code_linecount+1)

        final_code = []
        final_code.append(inside_loop_code)
        final_code.append(condition_code)
        final_code.append("JUMP ", line_count_start)

        return final_code
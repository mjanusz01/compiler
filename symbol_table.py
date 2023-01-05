from typing import Optional

class Procedure:
    def __init__(self, name):
        self.name = name

    def set_begin_offset(self, memory_offset):
        self.begin_memory_offset = memory_offset
    
    def set_end_offset(self, memory_offset):
        self.end_memory_offset = memory_offset

    def set_memory_traceback_offset(self, memory_offset):
        self.set_memory_traceback_offset = memory_offset

    def __repr__(self):
        return str(self.name)
    
    def set_command_list(self, command_list):
        self.command_list = command_list

    def print_command_list(self):
        for command in self.command_list:
            print(command)
    
    def get_name(self):
        print("zwrot ",self.name)
        return self.name

class Command:
    def __init__(self, type, arguments):
        self.type = type
        self.arguments = arguments
    
class Var:
    def __init__(self, name, memory_offset, in_procedure):
        self.name = name
        self.memory_offset = memory_offset
        self.initialized = False
        self.in_procedure = in_procedure
        self.proc_name = "-1"
    
    def set_proc_name(self, proc_name):
        self.proc_name = proc_name

    def __repr__(self):
        return "var name: " + str(self.name) + " memory : " + str(self.memory_offset) + " proc : " + str(self.in_procedure) + " proc name : " + str(self.proc_name)

class SymbolTable:
    def __init__(self):
        self.variables = []
        self.procedures = []
        self.memory_offset = 0

    def add_variable(self, name, in_proc):
        self.variables = self.variables + [Var(name, self.memory_offset, in_proc)]
        self.memory_offset = self.memory_offset + 1
    
    def add_procedure(self,name):
        self.procedures = self.procedures + [Procedure(name)]
        for var in self.variables:
            if var.in_procedure == True and var.proc_name == "-1":
                var.proc_name = name
    
    def find_procedure_by_name(self, name):
        for proc in self.procedures:
            if str(proc) == str(name):
                return proc
        return Procedure("none")
    
    def print_vars(self):
        for var in self.variables:
            print(var)
        print(" ")
        for proc in self.procedures:
            print("Procedura o nazwie ",proc)
            for com in proc.command_list:
                print(com)
                print(" ")
            print(" ")


    
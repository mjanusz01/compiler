from typing import Optional

class Procedure:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Procedure : " + str(self.name)
    
class Var:
    def __init__(self, name, memory_offset, in_procedure, proc_name):
        self.name = name
        self.memory_offset = memory_offset
        self.initialized = False
        self.in_procedure = in_procedure
        self.proc_name = proc_name
    
    def __repr__(self):
        return "var name: " + str(self.name) + " memory : " + str(self.memory_offset) + "proc : " + str(self.in_procedure) + "proc name : " + str(self.proc_name)

class SymbolTable:
    def __init__(self):
        self.variables = []
        self.procedures = []
        self.memory_offset = 0

    def add_variable(self, name):
        self.variables = self.variables + [Var(name, self.memory_offset)]
        self.memory_offset = self.memory_offset + 1
    
    def add_procedure(self,name):
        self.procedures = self.procedures + [Procedure(name)]
    
    def print_vars(self):
        for var in self.variables:
            print(var)
        print(" ")
        for proc in self.procedures:
            print(proc)
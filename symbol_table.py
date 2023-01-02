from typing import Optional

class Procedure:
    def __init__(self, name, memory_offset):
        self.name = name
        self.memory_offset = memory_offset

    def __repr__(self):
        return "Procedure {self.name}"
    
class Var:
    def __init__(self, name, procedure: Optional[Procedure], memory_offset):
        self.name = name
        self.memory_offset = memory_offset
        self.initialized = False
        self.procedure = procedure
    
    def __repr__(self):
        if not self.initialized:
            return "Uninitialized variable at {self.memory_offset}"

class SymbolTable:
    def __init__(self):
        self.variables = {}
        self.procedures = {}

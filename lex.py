from sly import Lexer, Parser
from symbol_table import SymbolTable, Var, Procedure
from code_generator import CodeGenerator
import sys

class CompilatorLexer(Lexer):
    
    tokens = {PROGRAM, IS, PROCEDURE,
    VAR, ENDIF,
    BEGIN, END, 
    IF, THEN, ELSE,
    WHILE, DO, ENDWHILE, REPEAT, UNTIL, 
    READ, WRITE,
    IDENTIFIER, ASSIGN,
    GT, LT, GET, LET, EQ, NEQ,
    NUM,
    PLUS, MINUS, MULTIPLY, DIVIDE, MODULO,
    LBR, RBR, SEMICOLON, COMMA
    }
    ignore = ' \t'
    
    @_(r'\[[^\]]*\]')
    def ignore_comment(self, t):
        self.lineno += t.value.count('\n')

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    PROGRAM = r"PROGRAM"
    PROCEDURE = r"PROCEDURE"
    ENDWHILE = r"ENDWHILE"
    IS = r"IS"
    VAR = r"VAR"
    BEGIN = r"BEGIN"
    ENDIF = r"ENDIF"
    END = r"END"
    IF = r"IF"
    THEN = r"THEN"
    ELSE = r"ELSE"

    WHILE = r"WHILE"
    DO = r"DO"
    
    REPEAT = r"REPEAT"
    UNTIL = r"UNTIL"

    READ = r"READ"
    WRITE = r"WRITE"

    IDENTIFIER = r"[_a-z]+"
    ASSIGN = r":="

    GT = r">"
    LT = r"<"
    GET = r">="
    LET = r"<="
    EQ = r"="
    NEQ = r"!="

    PLUS = r"\+"
    MINUS = r"-"
    MULTIPLY = r"\*"
    DIVIDE = r"\/"
    MODULO = r"\%"

    LBR = r"\("
    RBR = r"\)"
    SEMICOLON = r";"
    COMMA = r","

    @_(r'\d+')
    def NUM(self, t):
        t.value = int(t.value)
        return t

class CompilatorParser(Parser):
    tokens = CompilatorLexer.tokens
    literals = CompilatorLexer.literals
    commands_list = []
    proc_command_list = []
    temp_list = []
    symbol_table = SymbolTable()
    in_procedure = True
    in_command = False
    processed_procedure = "pa"
    @_('procedures main')
    def whole_program(self, p):
        return "PROGRAM"
    
    @_('PROCEDURE proc_head IS VAR proc_declarations BEGIN commands END procedures2')
    def procedures(self, p):
        print("procedura o nazwie ", p[1])
        print("procedura aktualna ", self.processed_procedure)
        #print(p[1])
        #print("ODPOWIEDZ",self.symbol_table.find_procedure_by_name(p[1]))
        #self.symbol_table.find_procedure_by_name(self.processed_procedure).set_command_list(self.proc_command_list)
        #print("komendy lista", self.proc_command_list)
        #self.proc_command_list = []
        return "PROCEDURE"

    @_('PROCEDURE proc_head IS VAR proc_declarations BEGIN commands END procedures2')
    def procedures2(self, p):
        print("procedura o nazwie ", p[1])
        print("procedura aktualna ", self.processed_procedure)
        #print(p[1])
        #print("ODPOWIEDZ",self.symbol_table.find_procedure_by_name(p[1]))
        #self.symbol_table.find_procedure_by_name(self.processed_procedure).set_command_list(self.proc_command_list)
        #print("komendy lista", self.proc_command_list)
        #self.proc_command_list = []
        return "PROCEDURE"    

    @_('PROCEDURE proc_head IS BEGIN commands END procedures2')
    def procedures(self, p):
        #print("procedura o nazwie ", p[1])
        #print("procedura aktualna ", self.processed_procedure)
        #self.symbol_table.find_procedure_by_name(self.processed_procedure).set_command_list(self.proc_command_list)
        #print("komendy lista", self.proc_command_list)
        #self.proc_command_list = []
        return "PROCEDURE"

    @_('PROCEDURE proc_head IS BEGIN commands END procedures2')
    def procedures2(self, p):
        #print("procedura o nazwie ", p[1])
        #print("procedura aktualna ", self.processed_procedure)
        #self.symbol_table.find_procedure_by_name(self.processed_procedure).set_command_list(self.proc_command_list)
        #print("komendy lista", self.proc_command_list)
        #self.proc_command_list = []
        return "PROCEDURE"    
    
    @_('')
    def procedures2(self, p):
        print("empty")
        self.in_procedure = False
        self.symbol_table.find_procedure_by_name(self.processed_procedure).set_command_list(self.proc_command_list)
        return "EMPTY PROCEDURE"

    @_('')
    def procedures(self, p):
        print("empty")
        self.in_procedure = False
        return "EMPTY PROCEDURE"    

    @_('PROGRAM IS VAR declarations BEGIN commands END')
    def main(self, p):
        return "MAIN PROGRAM"

    @_('identifier LBR proc_declarations RBR')
    def proc_head(self, p):
        print("set name ", p[0])
        self.symbol_table.add_procedure(p[0])
        self.symbol_table.find_procedure_by_name(self.processed_procedure).set_command_list(self.proc_command_list)
        self.processed_procedure = p[0]
        self.proc_command_list = []
        return p[0]

    @_('proc_declarations COMMA proc_id')
    def proc_declarations(self, p):
        return "EEE"

    @_('proc_id')
    def proc_declarations(self,p):
        return "EEEE"
        
    @_('exec_id LBR exec_declarations RBR')
    def proc_head_execute(self, p):
        return p[0]

    @_('IDENTIFIER')
    def proc_id(self, p):
        self.symbol_table.add_variable(p[0],True)
        return "EXEC"

    @_('exec_declarations COMMA exec_id')
    def exec_declarations(self, p):
        self.temp_list.append(p[2])
        return [p[0], p[2]]

    @_('exec_id')
    def exec_declarations(self, p):
        self.temp_list.append(p[0])
        return p[0]

    @_('IDENTIFIER')
    def exec_id(self,p):
        return p[0]

    @_('declarations COMMA identifier')
    def declarations(self, p):
        self.symbol_table.add_variable(p[2], False)
        return "DECLARATIONS"

    @_('identifier')
    def declarations(self, p):
        self.symbol_table.add_variable(p[0], False)
        return "DECLARATIONS"

    @_('commands command')
    def commands(self, p):
        return p[0], p[1]

    @_('command')
    def commands(self, p):
        return p[0]

    @_('command2')
    def commands2(self,p):
        return p[0]

    @_('commands2 command2')
    def commands2(self, p):
        return p[0], p[1]

    @_('identifier ASSIGN expression SEMICOLON')
    def command(self, p):
        if not self.in_command:
            if self.in_procedure:
                self.proc_command_list = self.proc_command_list + ["ASSIGN", p[0], p[2]]
            else:
                self.commands_list = self.commands_list + ["ASSIGN", p[0], p[2]]
                self.commands_list.append(["ASSIGN", p[0], p[2]])
        return "ASSIGN", p[0], p[2]

    @_('IF condition THEN commands2 ELSE commands2 ENDIF')
    def command(self, p):
        if not self.in_command:
            self.in_command = True
            if self.in_procedure:
                print("appendujemy")
                self.proc_command_list.append(["ifelse", p[1], p[3], p[5]])
            else:
                self.commands_list.append(["ifelse", p[1], p[3], p[5]])
            self.in_command = False
        return "ifelse", p[1], p[3], p[5]

    @_('IF condition THEN commands2 ENDIF')
    def command(self, p):
        if not self.in_command:
            self.in_command = True
            if self.in_procedure:
                self.proc_command_list.append(["IF", p[1], p[3]])
            else:
                self.commands_list.append(["IF", p[1], p[3]])
            self.in_command = False

    @_('WHILE condition DO commands2 ENDWHILE')
    def command(self, p):
        if not self.in_command:
            self.in_command = True
            if self.in_procedure:
                self.proc_command_list.append(["WHILE",p[1],p[3]])
            else:
                self.commands_list.append(["WHILE",p[1],p[3]])
            self.in_command = False
        return "WHILE"

    @_('REPEAT commands2 UNTIL condition SEMICOLON')
    def command(self, p):
        print("AKTUALNIE ",self.in_procedure)
        if self.in_procedure:
            self.proc_command_list.append(["until", p[1], p[3]])
        else:
            self.commands_list.append(["until",p[1], p[3]])
        return "UNTILREPEAT"
    
    @_('proc_head_execute SEMICOLON')
    def command(self, p):
        if self.in_procedure:
            print("EXECUTE ", p[0])
            self.proc_command_list.append(["proc", p[0], self.temp_list])
            print(self.proc_command_list)
            self.temp_list = []
        else:
            self.commands_list.append(["proc", p[0], self.temp_list])
            self.temp_list = []
        return "PROC_HEAD SEMICOLON"
    
    @_('READ identifier SEMICOLON')
    def command(self, p):
        if self.in_procedure:
            self.proc_command_list.append(["read", p[1]])
        else:
            self.commands_list.append(["read", p[1]])
        return "READ", p[1]

    @_('WRITE value SEMICOLON')
    def command(self, p):
        print("WRITE aktualnie")
        if self.in_procedure:
            self.proc_command_list.append(["WRITE", p[1]])
        else:
            self.commands_list.append(["WRITE", p[1]])
        return "WRITE", p[1]

    @_('identifier ASSIGN expression SEMICOLON')
    def command2(self, p):
        return "ASSIGN", p[0], p[2]

    @_('IF condition THEN commands2 ELSE commands2 ENDIF')
    def command2(self, p):
        return "ifelse", p[1], p[3], p[5]

    @_('IF condition THEN commands2 ENDIF')
    def command2(self, p):
        return "if", p[1], p[3]

    @_('WHILE condition DO commands2 ENDWHILE')
    def command2(self, p):
        return "WHILE", p[1], p[3]

    @_('REPEAT commands2 UNTIL condition SEMICOLON')
    def command2(self, p):
        return "UNTIL", p[1], p[3]
    
    @_('proc_head_execute SEMICOLON')
    def command2(self, p):
        temp_copy = self.temp_list.copy()
        self.temp_list = []
        return "proc", p[0], temp_copy
    
    @_('READ identifier SEMICOLON')
    def command2(self, p):
        return "READ", p[1]

    @_('WRITE value SEMICOLON')
    def command2(self, p):
        return "WRITE", p[1]

    @_('value')
    def expression(self, p):
        return p[0]

    @_('value PLUS value')
    def expression(self, p):
        return "ADD", p[0], p[2]

    @_('value MINUS value')
    def expression(self, p):
        return "SUBT", p[0], p[2]

    @_('value MULTIPLY value')
    def expression(self, p):
        return "MULT", p[0], p[2]

    @_('value DIVIDE value')
    def expression(self, p):
        return "DIV", p[0], p[2]

    @_('value MODULO value')
    def expression(self, p):
        return "MOD", p[0], p[2]

    @_('value EQ value')
    def condition(self, p):
        return "EQ", p[0], [2]

    @_('value NEQ value')
    def condition(self, p):
        return "NEQ", p[0], p[2]

    @_('value GT value')
    def condition(self, p):
        return "GT", p[0], p[2]

    @_('value LT value')
    def condition(self, p):
        return "LT", p[0], p[2]

    @_('value GET value')
    def condition(self, p):
        return "GEQ", p[0], p[2]

    @_('value LET value')
    def condition(self, p):
        return "LEQ", p[0], p[2]

    @_('NUM')
    def value(self, p):
        return "const", p[0]

    @_('identifier')
    def value(self, p):
        return "var", p[0]

    @_('IDENTIFIER')
    def identifier(self, p):
        return p[0]

    def write_commands(self):
        for com in self.commands_list:
            print(com)


lex = CompilatorLexer()
pars = CompilatorParser()


with open(sys.argv[1]) as in_f:
    text = in_f.read()

pars.parse(lex.tokenize(text))
print("comm")
#print(pars.processed_procedure)
#print(pars.proc_command_list)
#pars.symbol_table.print_vars()

pars.write_commands()

code_gen = CodeGenerator(pars.symbol_table)
code_gen.generate_code(pars.commands_list)


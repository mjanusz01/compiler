from sly import Lexer, Parser
from symbol_table import SymbolTable, Var, Procedure
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
    procedure_commands_list = []
    commands_list = []
    proc_command_list = []
    temp_list = []
    symbol_table = SymbolTable()
    processed_procedure = ""
    in_procedure = True

    @_('procedures main')
    def whole_program(self, p):
        return "PROGRAM"
    
    @_('procedures PROCEDURE proc_head IS VAR declarations BEGIN commands END')
    def procedures(self, p):
        print("procedura o nazwie ", p[2])
        self.processed_procedure = p[2]
        return "PROCEDURE"

    @_('procedures PROCEDURE proc_head IS BEGIN commands END')
    def procedures(self, p):
        print("procedura o nazwie ", p[2])
        self.processed_procedure = p[2]
        return "PROCEDURE"
    
    @_('')
    def procedures(self, p):
        return "EMPTY PROCEDURE"

    @_('PROGRAM IS VAR declarations BEGIN commands END')
    def main(self, p):
        in_procedure = False
        return "MAIN PROGRAM"

    @_('identifier LBR proc_declarations RBR')
    def proc_head(self, p):
        print("set name")
        self.symbol_table.add_procedure(p[0])
        self.processed_procedure = str(p[0])
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
        return [p[0], p[1]]

    @_('command')
    def commands(self, p):
        return p[0]

    @_('identifier ASSIGN expression SEMICOLON')
    def command(self, p):
        return "assign", p[0], p[2]

    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        if self.in_procedure:
            self.proc_command_list.append(["ifelse", p[1], p[3], p[5]])
        else:
            self.commands_list.append(["ifelse", p[1], p[3], p[5]])

    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        if self.in_procedure:
            self.proc_command_list.append(["if", p[1], p[3]])
        else:
            self.commands_list.append(["if", p[1], p[3]])

    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        if self.in_procedure:
            self.proc_command_list.append(["while",p[1],p[3]])
        else:
            self.commands_list.append(["while",p[1],p[3]])
        return "WHILE"

    @_('REPEAT commands UNTIL condition SEMICOLON')
    def command(self, p):
        if self.in_procedure:
            self.proc_command_list.append(["until", p[1], p[3]])
        else:
            self.commands_list.append(["until",p[1], p[3]])
        return "UNTILREPEAT"
    
    @_('proc_head_execute SEMICOLON')
    def command(self, p):
        if self.in_procedure:
            self.proc_command_list.append(["proc", p[0], self.temp_list])
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
        if self.in_procedure:
            self.proc_command_list.append(["write", p[1]])
        else:
            self.commands_list.append(["write", p[1]])
        return "write", p[1]

    @_('value')
    def expression(self, p):
        print(["load",p[0]])

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
        return "var_value", p[0]

    @_('IDENTIFIER')
    def identifier(self, p):
        return p[0]

    def write_commands(self):
        for com in self.commands_list:
            print(com)


lex = CompilatorLexer()
pars = CompilatorParser()
with open(sys.argv[1])  as in_f:
    text = in_f.read()

pars.parse(lex.tokenize(text))
pars.symbol_table.print_vars()
pars.write_commands()

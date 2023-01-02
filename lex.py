from sly import Lexer, Parser
from symbol_table import SymbolTable, Var, Procedure
import sys

class CompilatorLexer(Lexer):
    
    tokens = {PROGRAM, IS,
    PROCEDURE,
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
    ENDWHILE = r"ENDWHILE"
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
        print("tu wchodze")
        t.value = int(t.value)
        return t

class CompilatorParser(Parser):
    tokens = CompilatorLexer.tokens
    literals = CompilatorLexer.literals
    symbol_table = SymbolTable()

    @_('procedures main')
    def whole_program(self, p):
        print("program")
        return "PROGRAM"
    
    @_('procedures PROCEDURE proc_head IS VAR declarations BEGIN commands END')
    def procedures(self, p):
        return "PROCEDURE"

    @_('procedures PROCEDURE proc_head IS BEGIN commands END')
    def procedures(self, p):
        return "PROCEDURE"
    
    @_('')
    def procedures(self, p):
        print("empty procedure")
        return "EMPTY PROCEDURE"

    @_('PROGRAM IS VAR declarations BEGIN commands END')
    def main(self, p):
        return "MAIN PROGRAM"

    @_('identifier LBR declarations RBR')
    def proc_head(self, p):
        return "IDENTIFIER"
    
    @_('declarations COMMA identifier')
    def declarations(self, p):
        return "DECLARATIONS"

    @_('identifier')
    def declarations(self, p):
        return "DECLARATIONS"

    @_('commands command')
    def commands(self, p):
        return "COMMANDS"

    @_('command')
    def commands(self, p):
        return "COMMANDSLAST"

    @_('identifier ASSIGN expression SEMICOLON')
    def command(self, p):
        return "ASSIGN"

    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        print("ifelse")
        return "IFELSE"

    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        print("if")
        return "IF"

    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        return "WHILE"

    @_('REPEAT commands UNTIL condition SEMICOLON')
    def command(self, p):
        return "UNTILREPEAT"
    
    @_('proc_head')
    def command(self, p):
        return "PROC_HEAD SEMICOLON"
    
    @_('READ identifier SEMICOLON')
    def command(self, p):
        return "READ"

    @_('WRITE value SEMICOLON')
    def command(self, p):
        return "WRITE"

    @_('value')
    def expression(self, p):
        return "VALUE"

    @_('value PLUS value')
    def expression(self, p):
        return "ADD"

    @_('value MINUS value')
    def expression(self, p):
        return "SUBT"

    @_('value MULTIPLY value')
    def expression(self, p):
        return "MULT"

    @_('value DIVIDE value')
    def expression(self, p):
        return "DIV"

    @_('value MODULO value')
    def expression(self, p):
        return "MOD"

    @_('value EQ value')
    def condition(self, p):
        return "EQ"

    @_('value NEQ value')
    def condition(self, p):
        return "NEQ"

    @_('value GT value')
    def condition(self, p):
        return "GT"

    @_('value LT value')
    def condition(self, p):
        return "LT"

    @_('value GET value')
    def condition(self, p):
        return "GEQ"

    @_('value LET value')
    def condition(self, p):
        return "LEQ"

    @_('NUM')
    def value(self, p):
        print("jestem tu ", p[0])
        return "NUMVALUE"

    @_('identifier')
    def value(self, p):
        return "ID"

    @_('IDENTIFIER')
    def identifier(self, p):
        print("tu tez jestem", p[0])
        return "IDENTIFIER"

lex = CompilatorLexer()
pars = CompilatorParser()
with open(sys.argv[1])  as in_f:
    text = in_f.read()

pars.parse(lex.tokenize(text))
print(pars.symbol_table.procedures)
print(" ")
print(pars.symbol_table.variables)

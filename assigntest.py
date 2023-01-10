import unittest
import assign
from symbol_table import SymbolTable, Var, Procedure, Command

class AssignTest(unittest.TestCase):

    def var_assign_const_test(self):
        
        #setup
        test_command = ['ASSIGN', 'x',('const','10')]

        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('x',False)

        test_line_count = 100

        expected_code = ['SET 10', 'STORE 3']

        
        #when
        assign_code = assign.assign(test_command,test_symbol_table,test_line_count)

        #then
        self.assertEqual(expected_code,assign_code)

    def var_assign_var_test(self):

        #setup
        test_command = ['ASSIGN', 'x',('var','y')]

        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('x',False)
        test_symbol_table.add_variable('y',False)

        test_line_count = 100

        expected_code = ['LOAD 4', 'STORE 3']

        #when
        assign_code = assign.assign(test_command,test_symbol_table,test_line_count)

        #then
        self.assertEqual(expected_code,assign_code)

    def var_add_var_test(self):

        #setup
        test_command = ['ASSIGN', 'res',('ADD',('var','y'),('var','x'))]

        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('x',False)
        test_symbol_table.add_variable('y',False)
        test_symbol_table.add_variable('res',False)
        test_line_count = 100

        expected_code = ['LOAD 4', 'ADD 3', 'STORE 5']

        #when
        assign_code = assign.assign(test_command,test_symbol_table,test_line_count)

        #then
        self.assertEqual(expected_code,assign_code)

    def var_add_const_test(self):

        #setup
        test_command = ['ASSIGN', 'res',('ADD',('var','y'),('const','2'))]

        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('y',False)
        test_symbol_table.add_variable('res',False)
        test_line_count = 100

        expected_code = ['SET 2', 'ADD 3', 'STORE 4']

        #when
        assign_code = assign.assign(test_command,test_symbol_table,test_line_count)

        #then
        self.assertEqual(expected_code,assign_code)    

    def const_add_var_test(self):

        #setup
        test_command = ['ASSIGN', 'res',('ADD',('const','115'),('var','x'))]

        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('x',False)
        test_symbol_table.add_variable('res',False)
        test_line_count = 100

        expected_code = ['SET 115', 'ADD 3', 'STORE 4']

        #when
        assign_code = assign.assign(test_command,test_symbol_table,test_line_count)

        #then
        self.assertEqual(expected_code,assign_code) 

    def const_add_const_test(self):

        #setup
        test_command = ['ASSIGN', 'res',('ADD',('const','115'),('const','329'))]

        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('x',False)
        test_symbol_table.add_variable('res',False)
        test_line_count = 100

        expected_code = ['SET 115', 'STORE 1', 'SET 329', 'ADD 1', 'STORE 4']

        #when
        assign_code = assign.assign(test_command,test_symbol_table,test_line_count)

        #then
        self.assertEqual(expected_code,assign_code) 

    def var_subt_var_test(self):

        #setup
        test_command = ['ASSIGN', 'res',('SUBT',('var','y'),('var','x'))]

        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('x',False)
        test_symbol_table.add_variable('y',False)
        test_symbol_table.add_variable('res',False)
        test_line_count = 100

        expected_code = ['LOAD 4', 'SUB 3', 'STORE 5']

        #when
        assign_code = assign.assign(test_command,test_symbol_table,test_line_count)

        #then
        self.assertEqual(expected_code,assign_code)

    def var_subt_const_test(self):

        #setup
        test_command = ['ASSIGN', 'res',('SUBT',('var','y'),('const','2'))]

        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('y',False)
        test_symbol_table.add_variable('res',False)
        test_line_count = 100

        expected_code = ['SET 2', 'STORE 1', 'LOAD 3', 'SUB 1', 'STORE 4']

        #when
        assign_code = assign.assign(test_command,test_symbol_table,test_line_count)

        #then
        self.assertEqual(expected_code,assign_code)    

    def const_subt_var_test(self):

        #setup
        test_command = ['ASSIGN', 'res',('SUBT',('const','115'),('var','x'))]

        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('x',False)
        test_symbol_table.add_variable('res',False)
        test_line_count = 100

        expected_code = ['SET 115', 'SUB 3', 'STORE 4']

        #when
        assign_code = assign.assign(test_command,test_symbol_table,test_line_count)

        #then
        self.assertEqual(expected_code,assign_code) 

    def const_subt_const_test(self):

        #setup
        test_command = ['ASSIGN', 'res',('SUBT',('const','115'),('const','329'))]

        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('x',False)
        test_symbol_table.add_variable('res',False)
        test_line_count = 100

        expected_code = ['SET 115', 'STORE 1', 'SET 329', 'SUB 1', 'STORE 4']

        #when
        assign_code = assign.assign(test_command,test_symbol_table,test_line_count)

        #then
        self.assertEqual(expected_code,assign_code) 

    def const_mult_const_test(self):

        #setup
        test_command = ['ASSIGN', 'res',('MULT',('const','115'),('const','329'))]

        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('x',False)
        test_symbol_table.add_variable('res',False)
        test_line_count = 100

        expected_code = ['SET 329',
        'STORE 1',
        'STORE 4', 
        'LOAD 4',
        'HALF',
        'ADD 0',
        'STORE 3',
        'LOAD 4',
        'SUB 3',
        'JZERO 114',
        'LOAD 2',
        'ADD 1',
        'STORE 2',
        'LOAD 2',
        'ADD 2',
        'STORE 2',
        'LOAD 4',
        'HALF',
        'STORE 4',
        'JZERO 122',
        'JUMP 103']

        #when
        assign_code = assign.assign(test_command,test_symbol_table,test_line_count)

        #then
        self.assertEqual(expected_code,assign_code) 

test = AssignTest()
test.var_assign_const_test()
test.var_assign_var_test()
test.var_add_var_test()
test.var_add_const_test()
test.const_add_var_test()
test.const_add_const_test()
test.var_subt_var_test()
test.var_subt_const_test()
test.const_subt_var_test()
test.const_subt_const_test()
test.const_mult_const_test()


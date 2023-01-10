import unittest
import assign
from symbol_table import SymbolTable, Var, Procedure, Command
import condition

class ConditionTest(unittest.TestCase):

    def var_GT_var_test(self):

        #setup
        test_command = ('GT', ('var', 'i'), ('var', 'x'))
        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('x',False)
        test_symbol_table.add_variable('i',False)

        expected_code = ['LOAD 4', 'SUBT 3', 'JZERO [not]']

        #when
        assign_code = condition.double_arg_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

    def var_GT_const_test(self):

        #setup
        test_command = ('GT', ('var', 'i'), ('const', '2'))
        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('i',False)

        expected_code = ['SET 2', 'STORE 1', 'LOAD 3', 'SUBT 1', 'JZERO [not]']

        #when
        assign_code = condition.double_arg_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

    def const_GT_var_test(self):

        #setup
        test_command = ('GT', ('const', '111'), ('var', 'x'))
        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('x',False)

        expected_code = ['SET 111', 'SUBT 3', 'JZERO [not]']

        #when
        assign_code = condition.double_arg_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)
    
    def const_GT_const_returns_true_test(self):

        #setup
        test_command = ('GT', ('const', '12'), ('const', '10'))
        test_symbol_table = SymbolTable()
        expected_code = []

        #when
        assign_code = condition.double_arg_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

    def const_GT_const_returns_false_test(self):

        #setup
        test_command = ('GT', ('const', '12'), ('const', '13'))
        test_symbol_table = SymbolTable()
        expected_code = ['JZERO [not]']

        #when
        assign_code = condition.double_arg_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

    def var_LT_var_test(self):

        #setup
        test_command = ('LT', ('var', 'i'), ('var', 'x'))
        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('x',False)
        test_symbol_table.add_variable('i',False)

        expected_code = ['LOAD 3', 'SUBT 4', 'JZERO [not]']

        #when
        assign_code = condition.double_arg_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

    def var_LT_const_test(self):

        #setup
        test_command = ('LT', ('var', 'i'), ('const', '2'))
        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('i',False)

        expected_code = ['SET 2', 'SUBT 3', 'JZERO [not]']

        #when
        assign_code = condition.double_arg_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

    def const_LT_var_test(self):

        #setup
        test_command = ('LT', ('const', '111'), ('var', 'x'))
        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('x',False)

        expected_code = ['SET 111', 'STORE 1', 'LOAD 3', 'SUBT 1', 'JZERO [not]']

        #when
        assign_code = condition.double_arg_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)
    
    def const_LT_const_returns_true_test(self):

        #setup
        test_command = ('LT', ('const', '12'), ('const', '10'))
        test_symbol_table = SymbolTable()
        expected_code = ['JZERO [not]']

        #when
        assign_code = condition.double_arg_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

    def const_LT_const_returns_false_test(self):

        #setup
        test_command = ('LT', ('const', '12'), ('const', '13'))
        test_symbol_table = SymbolTable()
        expected_code = []

        #when
        assign_code = condition.double_arg_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

    def var_GET_var_test(self):

        #setup
        test_command = ('GET', ('var', 'i'), ('var', 'x'))
        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('x',False)
        test_symbol_table.add_variable('i',False)

        expected_code = ['LOAD 3', 'SUBT 4', 'JPOS [not]']

        #when
        assign_code = condition.double_arg_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

    def var_GET_const_test(self):

        #setup
        test_command = ('GET', ('var', 'i'), ('const', '2'))
        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('i',False)

        expected_code = ['SET 2', 'SUBT 3', 'JPOS [not]']

        #when
        assign_code = condition.double_arg_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

    def const_GET_var_test(self):

        #setup
        test_command = ('GET', ('const', '111'), ('var', 'x'))
        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('x',False)

        expected_code = ['SET 111', 'STORE 1', 'LOAD 3', 'SUBT 1', 'JPOS [not]']

        #when
        assign_code = condition.double_arg_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)
    
    def const_GET_const_returns_true_test(self):

        #setup
        test_command = ('GET', ('const', '12'), ('const', '10'))
        test_symbol_table = SymbolTable()
        expected_code = ['JPOS [not]']

        #when
        assign_code = condition.double_arg_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

    def const_GET_const_returns_false_test(self):

        #setup
        test_command = ('GET', ('const', '12'), ('const', '13'))
        test_symbol_table = SymbolTable()
        expected_code = []

        #when
        assign_code = condition.double_arg_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

    def var_LET_var_test(self):

        #setup
        test_command = ('LET', ('var', 'i'), ('var', 'x'))
        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('x',False)
        test_symbol_table.add_variable('i',False)

        expected_code = ['LOAD 4', 'SUBT 3', 'JPOS[not]']

        #when
        assign_code = condition.double_arg_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

    def var_LET_const_test(self):

        #setup
        test_command = ('LET', ('var', 'i'), ('const', '2'))
        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('i',False)

        expected_code = ['SET 2', 'STORE 1', 'LOAD 3', 'SUBT 1', 'JPOS [not]']

        #when
        assign_code = condition.double_arg_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

    def const_LET_var_test(self):

        #setup
        test_command = ('LET', ('const', '111'), ('var', 'x'))
        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('x',False)

        expected_code = ['SET 111', 'SUBT 3', 'JPOS [not]']

        #when
        assign_code = condition.double_arg_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)
    
    def const_LET_const_returns_true_test(self):

        #setup
        test_command = ('LET', ('const', '12'), ('const', '10'))
        test_symbol_table = SymbolTable()
        expected_code = []

        #when
        assign_code = condition.double_arg_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

    def const_LET_const_returns_false_test(self):

        #setup
        test_command = ('LET', ('const', '12'), ('const', '13'))
        test_symbol_table = SymbolTable()
        expected_code = ['JPOS [not]']

        #when
        assign_code = condition.double_arg_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

    def var_EQ_var_test(self):

        #setup
        test_command = ('EQ', ('var', 'i'), ('var', 'x'))
        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('x',False)
        test_symbol_table.add_variable('i',False)

        expected_code = ['LOAD 4', 'SUBT 3', 'JPOS [not]', 'LOAD 3', 'SUBT 4', 'JPOS [not]']

        #when
        assign_code = condition.eq_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

    def var_EQ_const_test(self):

        #setup
        test_command = ('EQ', ('var', 'i'), ('const', '2'))
        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('i',False)

        expected_code = ['SET 2','SUBT 3','JPOS [not]','SET 2','STORE 1','LOAD 3','SUBT 1','JPOS [not]']

        #when
        assign_code = condition.eq_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

    def const_EQ_var_test(self):

        #setup
        test_command = ('EQ', ('const', '111'), ('var', 'x'))
        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('x',False)

        expected_code = ['SET 111', 'SUBT 3', 'JPOS [not]','SET 111','STORE 1','LOAD 3','SUBT 1','JPOS [not]']

        #when
        assign_code = condition.eq_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)
    
    def const_EQ_const_returns_true_test(self):

        #setup
        test_command = ('EQ', ('const', '12'), ('const', '12'))
        test_symbol_table = SymbolTable()
        expected_code = []

        #when
        assign_code = condition.eq_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

    def const_EQ_const_returns_false_test(self):

        #setup
        test_command = ('EQ', ('const', '12'), ('const', '13'))
        test_symbol_table = SymbolTable()
        expected_code = ['JPOS [not]']

        #when
        assign_code = condition.eq_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

    def var_NEQ_var_test(self):

        #setup
        test_command = ('NEQ', ('var', 'i'), ('var', 'x'))
        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('x',False)
        test_symbol_table.add_variable('i',False)

        expected_code = ['LOAD 4', 'SUBT 3', 'JZERO [not]', 'LOAD 3', 'SUBT 4', 'JZERO [not]']

        #when
        assign_code = condition.eq_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

    def var_NEQ_const_test(self):

        #setup
        test_command = ('NEQ', ('var', 'i'), ('const', '2'))
        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('i',False)

        expected_code = ['SET 2','SUBT 3','JZERO [not]','SET 2','STORE 1','LOAD 3','SUBT 1','JZERO [not]']

        #when
        assign_code = condition.eq_condition(test_command,test_symbol_table)
        

        #then
        self.assertEqual(expected_code,assign_code)

    def const_NEQ_var_test(self):

        #setup
        test_command = ('NEQ', ('const', '111'), ('var', 'x'))
        test_symbol_table = SymbolTable()
        test_symbol_table.add_variable('x',False)

        expected_code = ['SET 111', 'SUBT 3', 'JZERO [not]','SET 111','STORE 1','LOAD 3','SUBT 1','JZERO [not]']

        #when
        assign_code = condition.eq_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)
    
    def const_NEQ_const_returns_true_test(self):

        #setup
        test_command = ('NEQ', ('const', '12'), ('const', '12'))
        test_symbol_table = SymbolTable()
        expected_code = []

        #when
        assign_code = condition.eq_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

    def const_NEQ_const_returns_false_test(self):

        #setup
        test_command = ('NEQ', ('const', '12'), ('const', '13'))
        test_symbol_table = SymbolTable()
        expected_code = ['JZERO [not]']

        #when
        assign_code = condition.eq_condition(test_command,test_symbol_table)

        #then
        self.assertEqual(expected_code,assign_code)

test = ConditionTest()

test.var_GT_var_test()
test.var_GT_const_test()
test.const_GT_var_test()
test.const_GT_const_returns_true_test()
test.const_GT_const_returns_false_test()

test.var_LT_var_test()
test.var_LT_const_test()
test.const_LT_var_test()
test.const_LT_const_returns_true_test()
test.const_LT_const_returns_false_test()

test.var_GET_var_test()
test.var_GET_const_test()
test.const_GET_var_test()
test.const_GET_const_returns_true_test()
test.const_GET_const_returns_false_test()

test.var_LET_var_test()
test.var_LET_const_test()
test.const_LET_var_test()
test.const_LET_const_returns_true_test()
test.const_LET_const_returns_false_test()

test.var_EQ_var_test()
test.var_EQ_const_test()
test.const_EQ_var_test()
test.const_EQ_const_returns_true_test()
test.const_EQ_const_returns_false_test()

test.var_NEQ_var_test()
test.var_NEQ_const_test()
test.const_NEQ_var_test()
test.const_NEQ_const_returns_true_test()
test.const_NEQ_const_returns_false_test()
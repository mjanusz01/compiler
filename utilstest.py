import unittest
import utils

class UtilsTest(unittest.TestCase):

    def replace_test(self):
        
        #given
        command_to_replace = ['SET 111', 'SUBT 3', 'JZERO [not]', 'SET 111', 'STORE 1', 'LOAD 3', 'SUBT 1', 'JZERO [not]']
        expression = "23"
        expected_command = ['SET 111', 'SUBT 3', 'JZERO 23', 'SET 111', 'STORE 1', 'LOAD 3', 'SUBT 1', 'JZERO 23']
        
        #when
        command = utils.replace(command_to_replace,"[not]",expression)

        #then
        self.assertEqual(command,expected_command)

    def linecount_test(self):
        #given
        command = ['SET 111', 'SUBT 3', 'JZERO [not]', 'SET 111', 'STORE 1', 'LOAD 3', 'SUBT 1', 'JZERO [not]']
        command_length = 8
        #when
        linecount = utils.linecount(command)

        #then
        self.assertEqual(linecount,command_length)

test = UtilsTest()

test.replace_test()
test.linecount_test()

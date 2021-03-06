import unittest
from cobalt_types import *
from cobalt_runner import evaluate, parse

class TestAddition(unittest.TestCase):
    def testAdditionInt(self):
        tests = [
            ('2 3+', [CobaltInt(5)]),
            ('-2 3+', [CobaltInt(1)]),
            ('2 -3+', [CobaltInt(-1)]),
            ('-2 -3+', [CobaltInt(-5)]),
        ]
        for input_string, resulting_stack in tests:
            stack = []
            evaluate(stack, parse(input_string))
            self.assertEqual(stack, resulting_stack)

    def testAdditionFloat(self):
        tests = [
            ('2.1 3.2+', [CobaltFloat('5.3')]),
            ('-2.1 3.2+', [CobaltFloat('1.1')]),
            ('2.1 -3.2+', [CobaltFloat('-1.1')]),
            ('-2.1 -3.2+', [CobaltFloat('-5.3')]),
        ]
        for input_string, resulting_stack in tests:
            stack = []
            evaluate(stack, parse(input_string))
            self.assertEqual(stack, resulting_stack)

if __name__ == '__main__':
    unittest.main()
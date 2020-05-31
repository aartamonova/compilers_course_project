import unittest
from lexer import lexer


def get_types(data):
    lexer.input(data)
    tokens = []
    while True:
        token = lexer.token()
        if not token:
            break
        tokens.append(token.type)
    return tokens


class TestLexer(unittest.TestCase):
    def test_parentheses(self):
        data = '''((()))'''
        types = get_types(data)
        expected = ['LPAREN', 'LPAREN', 'LPAREN',
                    'RPAREN', 'RPAREN', 'RPAREN']
        self.assertEqual(types, expected)

    def test_num_operations(self):
        data = '''+ - / * > < = mod'''
        types = get_types(data)
        expected = ['PLUS', 'MINUS', 'DIVIDE', 'MULTIPLY',
                    'GREATER', 'SMALLER', 'EQUAL', 'MOD']
        self.assertEqual(types, expected)

    def test_bool_operations(self):
        data = '''and or not'''
        types = get_types(data)
        expected = ['AND', 'OR', 'NOT']
        self.assertEqual(types, expected)

    def test_types(self):
        data = '''x xy1 123 -123 #t #f'''
        types = get_types(data)
        expected = ['ID', 'ID', 'NUMBER', 'NUMBER',
                    'BOOLEAN', 'BOOLEAN']
        self.assertEqual(types, expected)

    def test_reserved(self):
        data = '''define fun if'''
        types = get_types(data)
        expected = ['DEFINE', 'FUN', 'IF']
        self.assertEqual(types, expected)

    def test_id(self):
        data = '''1xy xy1'''
        types = get_types(data)
        expected = ['NUMBER', 'ID', 'ID']
        self.assertEqual(types, expected)

    def test_int_overflow(self):
        data = '''2147483648'''
        with self.assertRaises(OverflowError):
            get_types(data)

    def test_unexpected(self):
        data = '''a 1 ?'''
        with self.assertRaises(BaseException):
            get_types(data)

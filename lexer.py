import ply.lex as lex

reserved = ('MOD', 'DEFINE', 'FUN', 'IF', 'AND', 'OR', 'NOT')

tokens = ('PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'GREATER', 'SMALLER',
          'EQUAL', 'LPAREN', 'RPAREN', 'NUMBER', 'ID', 'BOOLEAN',
          'PRINT_NUM', 'PRINT_BOOL') + reserved

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_GREATER = r'>'
t_SMALLER = r'<'
t_EQUAL = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_BOOLEAN = r'\#[t|f]'
t_ignore = ' \r\t'


def t_NUMBER(t):
    r'[-]?\d+'
    try:
        t.value = int(t.value)
        if abs(t.value) > ((1 << 31) - 1):
            raise OverflowError("Integer overflow (%s), line %d" % (t.value, t.lineno))
    except ValueError:
        raise OverflowError("Integer overflow (%s), line %d" % (t.value, t.lineno))
    return t


def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9-]*'
    upper_value = t.value.upper()
    if upper_value in reserved:
        t.type = upper_value
    elif upper_value == 'PRINT-NUM':
        t.type = 'PRINT_NUM'
    elif upper_value == 'PRINT-BOOL':
        t.type = 'PRINT_BOOL'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise BaseException("Illegal character (%s)" % t.value[0])
    # t.lexer.skip(1)


lexer = lex.lex()

if __name__ == '__main__':
    data = '''+
    (+)a mod b print-num 999999
    + #t
    (+ 1 2)
    '''

    lexer.input(data)

    while True:
        token = lexer.token()
        if not token:
            break
        print(token)

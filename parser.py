import ply.yacc as yacc
from lexer import tokens
from ast import *


def p_program(p):
    '''program : stmt_list'''
    p[0] = Node('program', p[1])


def p_stmt_list(p):
    '''stmt_list : stmt_list stmt
                 | stmt'''
    if len(p) == 3:
        p[0] = Node('stmt_list', p[1], p[2])
    elif len(p) == 2:
        p[0] = p[1]


def p_stmt(p):
    '''stmt : expr
            | print_stmt
            | def_stmt'''
    p[0] = Node('stmt', p[1])


def p_def_stmt(p):
    '''def_stmt : LPAREN DEFINE var expr RPAREN'''
    p[0] = Node('def_stmt', p[3], p[4])


def p_var_stmt(p):
    '''var : id'''
    p[0] = Node('var', p[1])


def p_print_stmt(p):
    '''print_stmt : print_num
                  | print_bool'''
    p[0] = p[1]


def p_print_num_stmt(p):
    '''print_num : LPAREN PRINT_NUM expr RPAREN'''
    p[0] = Node('print_num', p[2], p[3])


def p_print_bool_stmt(p):
    '''print_bool : LPAREN PRINT_BOOL expr RPAREN'''
    p[0] = Node('print_bool', p[2], p[3])


def p_expr(p):
    '''expr : num_op
            | bool_op
            | if_expr
            | fun_expr
            | fun_call
            | number
            | boolean
            | id'''
    p[0] = Expr('expr', p[1])


def p_expr_list(p):
    '''expr_list : expr_list expr
                 | expr'''
    if len(p) == 3:
        p[0] = ExprList('expr_list', p[1], p[2])
    elif len(p) == 2:
        p[0] = p[1]


def p_if_expr(p):
    '''if_expr : LPAREN IF test_expr than_expr else_expr RPAREN'''
    p[0] = Node('if_expr', p[3], p[4], p[5])


def p_test_expr(p):
    '''test_expr : expr'''
    p[0] = TestExp('test_expr', p[1])


def p_than_expr(p):
    '''than_expr : expr'''
    p[0] = Node('than_expr', p[1])


def p_else_expr(p):
    '''else_expr : expr'''
    p[0] = Node('else_expr', p[1])


def p_fun_expr(p):
    '''fun_expr : LPAREN FUN LPAREN fun_ids RPAREN fun_body RPAREN'''
    p[0] = Node('fun_expr', p[4], p[6])


def p_fun_call(p):
    '''fun_call : LPAREN fun_expr fun_params RPAREN
                | LPAREN fun_name fun_params RPAREN'''
    p[0] = Node('fun_call', p[2], p[3])


def p_fun_name(p):
    '''fun_name : id'''
    p[0] = Node('fun_name', p[1])


def p_fun_ids(p):
    '''fun_ids : fun_ids fun_id
               | fun_id
               | '''
    if len(p) == 3:
        p[0] = Node('fun_ids', p[1], p[2])
    elif len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('fun_ids', 'nil')


def p_fun_id(p):
    '''fun_id : id'''
    p[0] = Node('fun_id', p[1])


def p_fun_params(p):
    '''fun_params : fun_params fun_param
                  | fun_param
                  | '''
    if len(p) == 3:
        p[0] = Node('fun_params', p[1], p[2])
    elif len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('fun_params', 'nil')


def p_fun_param(p):
    '''fun_param : expr'''
    p[0] = Node('fun_param', p[1])


def p_fun_body(p):
    '''fun_body : expr'''
    p[0] = Node('fun_body', p[1])


def p_num_op(p):
    '''num_op : num_two_op
              | num_more_op'''
    p[0] = p[1]


def p_num_two_op(p):
    '''num_two_op : LPAREN MINUS expr expr RPAREN
                  | LPAREN DIVIDE expr expr RPAREN
                  | LPAREN MOD expr expr RPAREN
                  | LPAREN GREATER expr expr RPAREN
                  | LPAREN SMALLER expr expr RPAREN'''
    p[0] = NumOp(p[2], p[3], p[4])


def p_num_more_op(p):
    '''num_more_op : LPAREN PLUS expr expr_list RPAREN
                   | LPAREN MULTIPLY expr expr_list RPAREN
                   | LPAREN EQUAL expr expr_list RPAREN'''
    p[0] = NumOp(p[2], p[3], p[4])


def p_bool_op(p):
    '''bool_op : and_or_op
               | not_op'''
    p[0] = p[1]


def p_and_or_op(p):
    '''and_or_op : LPAREN AND expr expr_list RPAREN
                 | LPAREN OR expr expr_list RPAREN'''
    p[0] = BoolOp(p[2], p[3], p[4])


def p_not_op(p):
    '''not_op : LPAREN NOT expr RPAREN'''
    p[0] = BoolOp(p[2], p[3])


def p_number(p):
    '''number : NUMBER'''
    p[0] = Node('number', str(p[1]))


def p_boolean(p):
    '''boolean : BOOLEAN'''
    p[0] = Node('boolean', str(p[1]))


def p_id(p):
    '''id : ID'''
    p[0] = Node('id', str(p[1]))


def p_error(p):
    if p:
        raise BaseException("Unexpected token at '%s'" % p.value)
    else:
        raise BaseException("Unexpected token at EOF")


parser = yacc.yacc()


def test_data(data, expected):
    print('String:', data)
    print('Expected:', expected)
    try:
        result = parser.parse(data)
    except Exception as error:
        print('Result: ERROR ' + str(error) + '\n')
        return
    else:
        print('Result: OK', '\n')
    ast = Tree(result)
    return ast


if __name__ == '__main__':
    # Проверка типов: сложить number и boolean
    lines = '''(+ 3 (not #t))'''
    test_data(lines, 'error')

    # Проверка типов: AND между number и boolean
    lines = '''(and (or #t #f) (+ 1 2))'''
    test_data(lines, 'error')

    # Проверка типов: если test_exr не boolean
    lines = '''(if 1 2 3)'''
    test_data(lines, 'error')

    # Условие
    lines = '''(if #t 2 (+ 1 2))'''
    test_data(lines, 'ok')

    # Несколько выражений
    lines = '''(+ 1 2) (and #t #f) (not #t)'''
    test_data(lines, 'ok')

    # Определение переменной
    lines = '''(define x 1)'''
    test_data(lines, 'ok')

    # Определение функции
    lines = '''(fun (x y z) (+ x y z))'''
    test_data(lines, 'ok')

    # Вызов функции
    lines = '''(foo 1 2)'''
    test_data(lines, 'ok')

    # Все вместе
    lines = '''
    (define foo
        (fun (x y)
            (if (not y)
            1
            (* x (foo (- x 1))))))
    '''
    test_data(lines, 'ok')

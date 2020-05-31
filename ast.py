import itertools
import uuid
from config import BaseConfig

from graphviz import Digraph

number_valid = ['number', 'id', 'fun_call', '+', '-', '*', '/', 'mod', '>', '<', '=']
boolean_valid = ['boolean', 'id', 'fun_call', 'and', 'or', 'not']


class Node(object):
    def __init__(self, node_type, *args):
        self.type = node_type
        self.args = args


class Expr(Node):
    def __init__(self, node_type, *args):
        super().__init__(node_type, *args)
        self.value_type = args[0].type


class ExprList(Node):
    def __init__(self, node_type, *args):
        super().__init__(node_type, *args)
        arg_types = [arg.value_type for arg in args]
        if not all(arg_type in number_valid for arg_type in arg_types):
            if not all(arg_type in boolean_valid for arg_type in arg_types):
                raise TypeError("All arguments must be of the same type")

        # Если у всех аргументов одинаковый тип, то неважно, какой из них выбрать
        self.value_type = args[0].value_type


class NumOp(Node):
    def __init__(self, node_type, *args):
        super().__init__(node_type, *args)
        arg_types = [arg.value_type for arg in args]

        # Все операнды должны быть number значениями или выражениями
        if not all(arg_type in number_valid for arg_type in arg_types):
            raise TypeError("Expect 'number' but got 'boolean'")


class BoolOp(Node):
    def __init__(self, node_type, *args):
        super().__init__(node_type, *args)
        arg_types = [arg.value_type for arg in args]

        # Все операнды должны быть boolean значениями или выражениями
        if not all(arg_type in boolean_valid for arg_type in arg_types):
            raise TypeError("Expect 'boolean' but got 'number'")


class TestExp(Node):
    def __init__(self, node_type, *args):
        super().__init__(node_type, *args)

        # test_expr должен быть boolean
        if args[0].value_type not in boolean_valid:
            raise TypeError("IF test expr: expect 'boolean' but got 'number'")


class Tree:
    def __init__(self, parser_output):
        self.ast = parser_output
        self.nodes = []
        self.edges = []

    def _build(self, node):
        if node is None:
            return None

        self.nodes.append([str(node), node.type])  # node_name, node_type
        for arg in node.args:
            if isinstance(arg, Node):
                self.edges.append([str(node), str(arg)])
                self._build(arg)
            else:
                self.nodes.append([str(node), node.type + '\n(' + arg + ')'])

    def draw(self):
        self._build(self.ast)
        try:
            filename = str(uuid.uuid4()) + '.gv'
            f = Digraph('AST', filename=filename, directory=BaseConfig.graphviz_dir)

            f.attr('node', {'shape': 'ellipse',
                            'fontname': 'segoe ui',
                            'fixedsize': 'true',
                            'width': '1.2',
                            'height': '0.8'})
            for node in self.nodes:
                f.node(node[0], node[1])

            for edge in self.edges:
                f.edge(edge[0], edge[1])

            f.render()
        except:
            print('Graph creation error')

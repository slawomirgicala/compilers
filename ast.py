class Node:
    pass


class Program(Node):
    def __init__(self, program):
        self.type = "program"
        self.program = program


class Statement(Node):
    def __init__(self, this_stmt, other_stmts):
        self.type = "statement"
        self.this_stmt = this_stmt
        self.other_stmts = other_stmts


class BinOp(Node):
    def __init__(self, left, op, right):
        self.type = "binop"
        self.left = left
        self.op = op
        self. right = right


class Number(Node):
    def __init__(self, value):
        self.type = "number"
        self.value = value


class Real(Node):
    def __init__(self, value):
        self.type = "real"
        self.value = value


class Text(Node):
    def __init__(self, value):
        self.type = "text"
        self.value = value


class Bool(Node):
    def __init__(self, value):
        self.type = "bool"
        self.value = value


class Variable(Node):
    def __init__(self, name, value):
        self.type = "variable"
        self.name = name
        self.value = value


class Assignment(Node):
    def __init__(self, name, value):
        self.type = "assignment"
        self.name = name
        self.value = value


class UnOp(Node):
    def __init__(self, op, value):
        self.type = "unop"
        self.op = op
        self.value = value


class Group(Node):
    def __init__(self, group):
        self.tye = "group"
        self.group = group
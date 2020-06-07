# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
# -----------------------------------------------------------------------------

import sys
import math

sys.path.insert(0, "../..")

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR'
}

tokens = [
    'NAME', 'NUMBER', 'REAL', 'LPAREN', 'RPAREN',# 'SQRT'#, 'SIN', 'COS', 'EXP', 'LOG',
    'EQUAL', 'NOTEQUAL', 'GREATER', 'LESS', 'GREATEREQUAL', 'LESSEQUAL',
    'BOOL', 'TEXT',
    'SQRT'
] + list(reserved.values())

literals = ['=', '+', '-', '*', '/', '(', ')', '^', ';']

# Tokens

def t_IF(t):
    r'if'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_FOR(t):
    r'for'
    return t

def t_SQRT(t):
    r'sqrt'
    return t

def t_BOOL(t):
    r'True|False'
    t.value = bool(t)
    return t

def t_TEXT(t):
    r'^"(\n|.)*"$'
    return t

t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
# t_LPAREN = r'\('
# t_RPAREN = r'\)'

t_EQUAL = r'=='
t_NOTEQUAL = r'!='
t_GREATER = r'>'
t_LESS = r'<'
t_GREATEREQUAL = r'>='
t_LESSEQUAL = r'<='


def t_REAL(t):
    r'(\d+\.\d+)|(\d+\.)|(\.\d+)'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)

    return t




t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
import lex as lex

lexer = lex.lex()

# Parsing rules

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('nonassoc', 'LESS', 'EQUAL', 'GREATER', 'LESSEQUAL', 'GREATEREQUAL'),
    ('right', '^'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}

import ast

def p_program(p):
    '''program : statements'''
    p[0] = ast.Program(p[1])


def p_statements_statement(p):
    '''statements : statements statement ";"
                | statement ";"'''
    if len(p) == 3:
        p[0] = ast.Statement(p[2], p[1])
    else:
        p[0] = ast.Statement(p[1], None)


def p_statement_assign(p):
    'statement : NAME "=" expression'
    names[p[1]] = p[3]
    p[0] = ast.Assignment(p[1], p[3])


def p_statement_expr(p):
    'statement : expression'
    print(p[1])


def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression '^' expression
                  | expression EQUAL expression
                  | expression NOTEQUAL expression
                  | expression GREATER expression
                  | expression LESS expression
                  | expression GREATEREQUAL expression
                  | expression LESSEQUAL expression'''
    # if p[2] == '+':
    #     p[0] = p[1] + p[3]
    # elif p[2] == '-':
    #     p[0] = p[1] - p[3]
    # elif p[2] == '*':
    #     p[0] = p[1] * p[3]
    # elif p[2] == '/':
    #     p[0] = p[1] / p[3]
    # elif p[2] == '^':
    #     p[0] = p[1] ** p[3]
    # elif p[2] == '==':
    #     p[0] = p[1] == p[3]
    # elif p[2] == '!=':
    #     p[0] = p[1] != p[3]
    # elif p[2] == '>':
    #     p[0] = p[1] > p[3]
    # elif p[2] == '<':
    #     p[0] = p[1] < p[3]
    # elif p[2] == '>=':
    #     p[0] = p[1] == p[3]
    # elif p[2] == '<=':
    #     p[0] = p[1] == p[3]

    p[0] = ast.BinOp(p[1], p[2], p[3])


# def p_expression_sqrt(p):
#     "expression : SQRT expression"
#     p[0] = math.sqrt(p[2])


def p_expression_uminus(p):
    '''expression : '-' expression %prec UMINUS
                  | SQRT expression %prec UMINUS'''
    if p[1] == '-':
        p[0] = -p[2]
    elif p[1] == 'sqrt':
        p[0] = math.sqrt(p[2])
    p[0] = ast.UnOp(p[1], p[2])


def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]
    p[0] = ast.Group(p[2])


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]
    p[0] = ast.Number(p[1])


def p_expression_real(p):
    "expression : REAL"
    p[0] = p[1]
    p[0] = ast.Real(p[1])


def p_expression_bool(p):
    "expression : BOOL"
    p[0] = p[1]
    p[0] = ast.Bool(p[1])


def p_expression_text(p):
    "expression : TEXT"
    p[0] = p[1]
    p[0] = ast.Text(p[1])


def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]
        p[0] = ast.Variable(p[1], names[p[1]])
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0




def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import yacc as yacc

parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s)

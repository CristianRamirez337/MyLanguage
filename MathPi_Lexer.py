import ply.lex as lex
import sys


tokens = [
    'ID', 'COLON', 'COMMA', 'DOT',
    'ASSIGN', 'DIVIDE', 'TIMES', 'MINUS', 'PLUS',
    'LT', 'GT', 'NE', 'NUMBER', 'PARL', 'PARR',
    'COMMENT', 'newline', 'STRING', 'EQ', 'SQBL', 'SQBR'
]

reserved = ['PROGRAM', 'END', 'VAR', 'PROCEDURE',
            'BEGIN', 'PRINT', 'INPUT', 'IF', 'ELSE', 'ENDIF',
            'WHILE', 'ENDW', 'DO', 'ENDDO', 'FOR', 'ENDF',
            'GOSUB', 'ENDP', 'FLOAT', 'INT', 'ARRAY_INT', 'ARRAY_FLOAT',
            'MATRIX_INT', 'MATRIX_FLOAT', 'CUBE_INT', 'CUBE_FLOAT',
            'IN', 'DWHILE', 'AND', 'OR', 'BOOL'
            ]

tokens = tokens + reserved

t_ignore = r' \t'
# t_newline = r'\n'
# t_ignore = '\t'
t_COLON = r':'
t_COMMA = r','
t_DOT = r'\.'
t_ASSIGN = r'='
t_DIVIDE = r'/'
t_TIMES = r'\*'
t_MINUS = r'\-'
t_PLUS = r'\+'
t_LT = r'<'
t_GT = r'>'
t_NE = r'!='
t_PARL = r'\('
t_PARR = r'\)'
t_EQ = r'={2}?'
t_SQBL = r'\['
t_SQBR = r'\]'


def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    if t.value.upper() in reserved:
        t.value = t.value.upper()
        t.type = t.value
    return t


def t_COMMENT(t):
    r'\#.*'
    pass


def t_NUMBER(t):
    r'-?([\d]*[\.][\d]+)|-?\d+'
    if str(t).find('.') != -1:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_STRING(t):
    r'["][a-zA-Z 0-9:!@#$%^&*()-+=/?<>,]+["]'
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

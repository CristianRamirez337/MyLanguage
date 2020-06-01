import ply.lex as lex
import ply.yacc as yacc
import sys

symbols = []
sym_type = []
count = 0


tokens = [
	'ID', 'COLON', 'COMMA', 'DOT',
	'ASSIGN', 'DIVIDE', 'TIMES', 'MINUS', 'PLUS',
	'LT', 'GT', 'NE', 'NUMBER', 'PARL', 'PARR',
	'COMMENT', 'newline', 'STRING', 'EQ', 'SQBL', 'SQBR'
]

reserved = ['PROGRAM', 'END', 'VAR', 'PROCEDURE',
	'BEGIN', 'PRINT', 'INPUT', 'IF', 'ELSE', 'ENDIF',
	'WHILE', 'ENDW', 'DO', 'ENDDO', 'FOR', 'ENDF',
	'GOSUB', 'ENDP', 'FLOAT', 'INT', 'ARRAY', 'MATRIX',
	'CUBE', 'IN', 'DWHILE'
]

tokens = tokens + reserved

t_ignore = r' \t'
#t_newline = r'\n'
#t_ignore = '\t'
t_COLON = r':'
t_COMMA= r','
t_DOT = r'\.'
t_ASSIGN = r'='
t_DIVIDE = r'/'
t_TIMES = r'\*'
t_MINUS = r'\-'
t_PLUS = r'\+'
t_LT = r'<'
t_GT = r'>'
t_NE = r'<>'
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
	r'\d+'
	t.value = int(t.value)
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)
	#pass

def t_STRING(t):
	r'["][a-zA-Z 0-9:!@#$%^&*()-+=/?<>,]+["]'
	return t

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

lexer = lex.lex()

#   ******************** YACC ***************

precedence = (
	('right', 'ASSIGN'),
	('left', 'NE'),
	('left', 'LT', 'GT'),
	('left', 'PLUS', 'MINUS'),
	('left', 'TIMES', 'DIVIDE'),
	('right', 'PARL'),
	('left', 'PARR')
)
# GENERAL PROGRAM
def p_program(p):
	''' program : PROGRAM COLON V P B END
	| PROGRAM COLON empty END'''

# VARIABLES
def p_V(p):
	''' V : V VAR VM COLON TIPO
	| empty'''


def p_VM(p):
	''' VM : ID VM2'''
	symbols.append(p[1])
	global count
	count += 1

def p_VM2(p):
	''' VM2 : COMMA ID VM2'''
	symbols.append(p[2])
	global count
	count += 1

def p_VM2_empty(p):
	'''VM2 : empty'''

# VARIABLE TYPE
def p_TIPO(p):
	''' TIPO : FLOAT
	| INT
	| ARRAY
	| MATRIX
	| CUBE'''
	global count
	for i in range(count):
		sym_type.append(p[1])
	count = 0

#PROCEDURES
def p_P(p):
	''' P : P PROCEDURE ID COLON B ENDP'''
	symbols.append(p[3])
	sym_type.append("PROCEDURE")

def p_P_empty(p):
	''' P : empty'''

# MAIN PROGRAM o INTERMADIATE CODE
def p_B(p):
	''' B : BEGIN COLON ST '''

def p_ST(p):
	''' ST : S ST
	| empty'''

# STATEMENTS
def p_S(p):
	''' S : PRINT PARL SID PARR
	| INPUT PARL IID PARR
	| IF CONDITION COLON ST ENDIF
	| IF CONDITION COLON ST ELSE COLON ST ENDIF
	| FOR ID IN ID COLON ST ENDF
	| VMC ASSIGN UPDATE
	| WHILE CONDITION COLON ST ENDW
	| DO COLON ST DWHILE COLON CONDITION ENDDO
	| GOSUB ID
	'''

# print management
def p_SID(p):
	'''SID : STRING SID2
	| VMC SID2'''
def p_SID2(p):
	'''SID2 : PLUS VMC SID2
	| PLUS STRING SID2
	| empty'''

# input management
def p_IID(p):
	'''IID : VMC IID2'''
def p_IID2(p):
	'''IID2 : COMMA VMC  IID2
	| empty'''

# if management
def p_CONDITION(p):
	'''CONDITION : CMP COMPARATOR CMP'''
def p_CMP(p):
	'''CMP : NUMBER
	| ID'''
def p_COMPARATOR(p):
	'''COMPARATOR : NE
	| GT
	| LT
	| EQ'''

# ASSIGN management
def p_VMC(p):
	'''VMC : ID
	| ID SQBL CMP SQBR SQBL CMP SQBR
	| ID SQBL CMP SQBR SQBL CMP SQBR SQBL CMP SQBR'''
# Definicion de cuadruplos
def p_UPDATE(p):
	'''UPDATE : VMC UPDATE
	| NUMBER OPERATOR UPDATE
	| VMC
	| NUMBER'''
def p_OPERATOR(p):
	'''OPERATOR : PLUS
	| MINUS
	| TIMES
	| DIVIDE'''

# def p_Sempty(p):
# 	''' S : empty '''

# EMPTY VALUES
def p_empty(p):
	''' empty :	'''
	pass

# THROWING ERROR
def p_error(p):
	print("\tSyntax error in line " + str(p.lineno))

parser = yacc.yacc()
f = open("CodigoIntermedio.txt", "r")
parser.parse(f.read())

for i in range(len(symbols)):
	print(str(sym_type[i]) + "\t\t" + str(symbols[i]))
#print(symbols)
#print(sym_type)
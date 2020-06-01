from MathPi_Lexer import tokens
from collections import deque
import ply.yacc as yacc


program_instructions = []
programCounter = 0

# -----------------------------------~ YACC ~-----------------------------------

precedence = (
    ('right', 'ASSIGN'),
    ('left', 'NE'),
    ('left', 'LT', 'GT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'PARL'),
    ('left', 'PARR')
)


# -----------------------------------< GENERAL PROGRAM >-----------------------------------
def p_program(p):
    ''' program : PROGRAM COLON V MAIN P B END'''

def p_MAIN(p):
    ''' MAIN : empty'''
    global programCounter
    program_instructions.append("Goto ")
    programCounter += 1
# --------------------------------< END OF GENERAL PROGRAM >--------------------------------


# -----------------------------------< VARIABLES >-----------------------------------
symbols = {}

def p_V(p):
    ''' V : V VAR VM COLON TIPO
    | empty'''


def p_VM(p):
    ''' VM : ID VM2'''
    symbols[p[1]] = ["NULL", "TYPE"]



def p_VM2(p):
    ''' VM2 : COMMA ID VM2'''
    symbols[p[2]] = ["NULL", "TYPE"]



def p_VM2_empty(p):
    '''VM2 : empty'''


# +++++++++++++++ / VARIABLE TYPE \ +++++++++++++++
def p_TIPO(p):
    ''' TIPO : FLOAT
    | INT
    | ARRAY
    | MATRIX
    | CUBE
    | BOOL'''
    for i in symbols:
        if symbols[i][1] == "TYPE":
            symbols[i][1] = p[1]

# -----------------------------------< END OF VARIABLES >-----------------------------------


# -----------------------------------< PROCEDURES >-----------------------------------
proceduresPos = deque()

def p_P(p):
    ''' P : P  AUXPOSP PROCEDURE ID COLON B ENDP'''
    global programCounter
    symbols[p[4]] = [proceduresPos.popleft(), "PROCEDURE"]
    program_instructions.append('END PROCEDURE')
    programCounter += 1
    program_instructions[0] = "Goto " + str(programCounter)


def p_P_empty(p):
    ''' P : empty'''
    program_instructions[0] = "Goto " + str(programCounter)


def p_AUXPOSP(p):
    ''' AUXPOSP : empty'''
    proceduresPos.append(programCounter)

# -----------------------------------< END OF PROCEDURES >-----------------------------------


# ------------------------------< MAIN PROGRAM or INTERMADIATE CODE >------------------------------
def p_B(p):
    ''' B : BEGIN COLON ST '''


def p_ST(p):
    ''' ST : S ST
    | empty'''
# ---------------------------< END OF MAIN PROGRAM or INTERMADIATE CODE >---------------------------


# -----------------------------------< STATEMENTS >-----------------------------------
def p_S(p):
    ''' S : FOR ID IN ID COLON ST ENDF
    | DO COLON ST DWHILE COLON CONDITION ENDDO
    '''

# +++++++++++++++ / SUBROUTINES \ +++++++++++++++
def p_S_GOSUB(p):
    ''' S : GOSUB ID'''
    global programCounter
    program_instructions.append('GOSUB ' + p[2])
    programCounter += 1
# +++++++++++++++ / PRINT MANAGEMENT \ +++++++++++++++
stringsL = ''


def p_S_PRINT(p):
    '''S : PRINT PARL SID PARR'''
    global programCounter, stringsL
    program_instructions.append(['PRINT', stringsL])
    programCounter += 1
    stringsL = ''


def p_SID(p):
    '''SID : SID PLUS SID_T'''


def p_SID2(p):
    '''SID : SID_T'''


def p_SID_T(p):
    '''SID_T : STRING
    | ID'''
    global stringsL
    stringsL = stringsL + str(p[1])

# def p_SID2(p):
#     '''SID2 : SID2 PLUS VMC
#     | SID2 PLUS STRING'''
#     global stringsL
#     stringsL = stringsL + str(p[1])


def p_SID2_empty(p):
    '''SID : empty'''

# To accept arrays, cubes and ID alone
# def p_VMC(p):
#     '''VMC : ID
#     | ID SQBL CMP SQBR SQBL CMP SQBR
#     | ID SQBL CMP SQBR SQBL CMP SQBR SQBL CMP SQBR'''


def p_CMP(p):
    '''CMP : ID'''
    operandsStack.append('-' + p[1])


# +++++++++++++++ / INPUT MANAGEMENT \ +++++++++++++++
def p_S_INPUT(p):
    '''S : INPUT PARL ID PARR'''
    global programCounter
    program_instructions.append("INPUT " + p[3])
    programCounter += 1

# def p_IID(p):
#     '''IID : VMC IID2'''
#
#
# def p_IID2(p):
#     '''IID2 : COMMA VMC  IID2
#     | empty'''


# +++++++++++++++++++++/ ASSIGN OR UPDATE MANAGEMENT \++++++++++++++++++++++
'''
	E->E+-T; E->T; T->T*/F; T->F; F->id; F->(E)
'''


def p_S_ASSIGN(p):
    ''' S : CMP ASSIGN UPDATE'''
    quadruple_generation(p[2])


def p_update(p):
    '''UPDATE : T '''


def p_update2(p):
    '''UPDATE : UPDATE PLUS T
    | UPDATE MINUS T
    | UPDATE OR T'''
    quadruple_generation(p[2])


def p_T(p):
    '''T : F'''


def p_T2(p):
    '''T : T TIMES F
    | T DIVIDE F
    | T AND F
    '''
    quadruple_generation(p[2])


def p_F(p):
    '''F : ID'''
    if p[1] in symbols:
        operandsStack.append('-' + p[1])
    else:
        print("Variable '" + p[1] + "' not declared yet")


def p_F_NUMBER(p):
    '''F : NUMBER'''
    operandsStack.append(p[1])

def p_FtoE(p):
    '''F : PARL CONDITION PARR'''


# +++++++++++++++++++++/ IF MANAGEMENT \++++++++++++++++++++++
def p_S_IF(p):
    '''S : IF CONDITION AUXCOLON ST ENDIF'''
    global programCounter
    programCounter += 1
    program_instructions.append('Goto ' + str(programCounter))

    aux = goToFPosition.pop()
    aux2 = program_instructions[aux].find(' - ')
    program_instructions[aux] = program_instructions[aux][0:aux2 + 1] + str(programCounter)

def p_S_IF2(p):
    '''S : IF CONDITION AUXCOLON ST ELSE COLON AUXQ ST AUXENDIF ENDIF'''


# AUX to adjust quadruple stack and insert the Goto after the true statements and to modify the go to false
def p_AUXQ(p):
    '''AUXQ : empty'''
    global programCounter
    programCounter += 1
    program_instructions.append('Goto ')
    firstInstructionCondition.append(programCounter)

    aux = goToFPosition.pop()
    aux2 = program_instructions[aux].find(' - ')
    program_instructions[aux] = program_instructions[aux][0:aux2 + 1] + str(programCounter)

def p_AUXENDIF(p):
    '''AUXENDIF : empty'''
    global programCounter
    programCounter += 1
    program_instructions.append('Goto ' + str(programCounter))

    aux = firstInstructionCondition.pop()
    program_instructions[aux - 1] = 'Goto ' + str(programCounter)


# +++++++++++++++++++++/ WHILE MANAGEMENT \++++++++++++++++++++++
def p_S_WHILE(p):
    ''' S : WHILE AUXWHILE CONDITION AUXCOLON ST AUXENDWHILE ENDW'''


def p_AUXWHILE(p):
    '''AUXWHILE : empty'''
    firstInstructionCondition.append(programCounter)

def p_AUXENDWHILE(p):
    '''AUXENDWHILE : empty'''
    global programCounter
    program_instructions.append('Goto ' + str(firstInstructionCondition.pop()))
    programCounter += 1

    aux = goToFPosition.pop()
    aux2 = program_instructions[aux].find(' - ')
    program_instructions[aux] = program_instructions[aux][0:aux2 + 1] + str(programCounter)



# +++++++++++++++++++++/ QUADRUPLES DEFINITION \++++++++++++++++++++++
# Quadruples stacks variables
operandsStack = deque()
executionQueue = []  # List to store quadruples
availTemporales = deque(['T1'])
availAux = [] # Temporal in use
iAvail = 2  # Execution index


# Looking for existing avails
def existingAvail(value):
    try:
        availAux.index(value)
        availTemporales.append(value)
        availAux.remove(value)
    except:
        pass

def quadruple_generation(operator):
    global iAvail
    executionQueue.append(operator)
    # Operands
    auxOperand = operandsStack.pop()
    executionQueue.append(operandsStack.pop())

    existingAvail(executionQueue[-1])  # Operand equal to a temporal

    executionQueue.append(auxOperand)

    existingAvail(executionQueue[-1])  # Operand equal to a temporal

    if operator != '=':
        operandsStack.append(availTemporales.popleft())
        executionQueue.append(operandsStack[-1])
        availAux.append(operandsStack[-1])
        availTemporales.append('T' + str(iAvail))  # New temporal
        iAvail += 1

    #print(executionQueue)

    global programCounter
    program_instructions.append(executionQueue[:])
    programCounter += 1

    executionQueue.clear()


# +++++++++++++++++++++/ CONDITION MANAGEMENT \++++++++++++++++++++++
firstInstructionCondition = []
goToFPosition = []


def p_CONDITION(p):
    '''CONDITION : UPDATE'''


def p_CONDITION2(p):
    '''CONDITION : UPDATE NE UPDATE
    | UPDATE GT UPDATE
    | UPDATE LT UPDATE
    | UPDATE EQ UPDATE'''
    quadruple_generation(p[2])


# +++++++++++++++++++++/ AUXCOLON MANAGEMENT \++++++++++++++++++++++
def p_AUXCOLON(p):
    '''AUXCOLON : COLON'''
    go2F()


def go2F():
    global programCounter
    program_instructions.append("GotoF~" + str(program_instructions[-1][-1]) + " - ")
    goToFPosition.append(programCounter)
    programCounter += 1


# ---------------------------------< END STATEMENTS >---------------------------------


def p_empty(p):
    ''' empty :	'''
    pass

# THROWING ERROR
def p_error(p):
    print("\tSyntax error in line " + str(p.lineno))


parser = yacc.yacc()
#f = open("codigoIntermedio2.txt", "r")
#f = open("RAICES", "r")
#f = open("DIGITS.txt", "r")
f = open("recursion.txt", "r")
parser.parse(f.read())


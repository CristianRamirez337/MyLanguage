from MathPi_Lexer import tokens
from collections import deque
import ply.yacc as yacc

program_instructions = []
program_counter = 0

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
    global program_counter
    program_instructions.append("Goto ")
    program_counter += 1


# --------------------------------< END OF GENERAL PROGRAM >--------------------------------


# -----------------------------------< VARIABLES >-----------------------------------
symbols = {}


def p_V(p):
    ''' V : V VAR VM COLON TIPO
    | empty'''


def p_VM(p):
    ''' VM : ID VM2'''
    symbols[p[1]] = ["NULL", "TYPE"]


def p_VM_array(p):
    ''' VM : ID SQBL NUMBER SQBR VM2'''
    symbols[p[1]] = ["NULL", "TYPE", p[3]]


def p_VM_matrix(p):
    ''' VM : ID SQBL NUMBER COMMA NUMBER SQBR VM2'''
    symbols[p[1]] = ["NULL", "TYPE", [p[3], p[5]]]


def p_VM_cube(p):
    ''' VM : ID SQBL NUMBER COMMA NUMBER COMMA NUMBER SQBR VM2'''
    symbols[p[1]] = ["NULL", "TYPE", [p[3], p[5], p[7]]]


def p_VM2(p):
    ''' VM2 : COMMA ID VM2'''
    symbols[p[2]] = ["NULL", "TYPE"]


def p_VM2_array(p):
    ''' VM2 : COMMA ID SQBL NUMBER  SQBR VM2'''
    symbols[p[2]] = ["NULL", "TYPE", p[4]]


def p_VM2_matrix(p):
    ''' VM2 : COMMA ID SQBL NUMBER COMMA NUMBER SQBR VM2'''
    symbols[p[2]] = ["NULL", "TYPE", [p[4], p[6]]]


def p_VM2_cube(p):
    ''' VM2 : COMMA ID SQBL NUMBER COMMA NUMBER COMMA NUMBER SQBR VM2'''
    symbols[p[2]] = ["NULL", "TYPE", [p[4], p[6], p[8]]]


def p_VM2_empty(p):
    '''VM2 : empty'''


# +++++++++++++++ / VARIABLE TYPE \ +++++++++++++++
def p_TIPO(p):
    ''' TIPO : FLOAT
    | INT
    | ARRAY_INT
    | ARRAY_FLOAT
    | MATRIX_INT
    | MATRIX_FLOAT
    | CUBE_INT
    | CUBE_FLOAT
    | BOOL'''
    for i in symbols:
        if symbols[i][1] == "TYPE":
            symbols[i][1] = p[1]


# -----------------------------------< END OF VARIABLES >-----------------------------------


# -----------------------------------< PROCEDURES >-----------------------------------
proceduresPos = deque()


def p_P(p):
    ''' P : P  AUXPOSP PROCEDURE ID COLON B ENDP'''
    global program_counter
    symbols[p[4]] = [proceduresPos.popleft(), "PROCEDURE"]
    program_instructions.append('END PROCEDURE')
    program_counter += 1
    program_instructions[0] = "Goto " + str(program_counter)


def p_P_empty(p):
    ''' P : empty'''
    program_instructions[0] = "Goto " + str(program_counter)


def p_AUXPOSP(p):
    ''' AUXPOSP : empty'''
    proceduresPos.append(program_counter)


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
    global program_counter
    program_instructions.append('GOSUB ' + p[2])
    program_counter += 1


# +++++++++++++++ / PRINT MANAGEMENT \ +++++++++++++++
stringsL = ''
string_id = []


def p_S_PRINT(p):
    '''S : PRINT PARL SID PARR'''
    global program_counter, stringsL
    # if stringsL:
    program_instructions.append(['PRINT', stringsL])
    stringsL = ''
    # else:
    #     program_instructions.append(['PRINT', string_id])
    program_counter += 1



def p_SID(p):
    '''SID : SID PLUS SID_T'''


def p_SID2(p):
    '''SID : SID_T'''


def p_SID_T(p):
    '''SID_T : STRING
    | ID'''
    global stringsL
    stringsL = stringsL + str(p[1])


# def p_SID_T_id(p):
#     '''SID_T : ID'''
#     string_id.append(p[1])

def p_SID2_empty(p):
    '''SID : empty'''


# +++++++++++++++ / INPUT MANAGEMENT \ +++++++++++++++
# ID number is to get if the value inside the square brackets is an id or a number
id_number = ''


def p_S_input(p):
    '''S : INPUT PARL ID PARR'''
    global program_counter
    program_instructions.append("INPUT " + p[3])
    program_counter += 1


def p_S_input_array_id(p):
    '''S : INPUT PARL ID SQBL IDNUM SQBR PARR'''
    global program_counter, id_number
    program_instructions.append("INPUT-ARRAY " + p[3] + '[' + str(id_number) + ']')
    program_counter += 1
    id_number = ''


def p_S_input_matrix_id(p):
    '''S : INPUT PARL ID SQBL IDNUM COMMA IDNUM SQBR PARR'''
    global program_counter, id_number
    program_instructions.append("INPUT-MATRIX " + p[3] + '[' + str(id_number) + ']')
    program_counter += 1
    id_number = ''


def p_S_input_cube_id(p):
    '''S : INPUT PARL ID SQBL IDNUM COMMA IDNUM COMMA IDNUM SQBR PARR'''
    global program_counter, id_number
    program_instructions.append("INPUT-CUBE " + p[3] + '[' + str(id_number) + ']')
    program_counter += 1
    id_number = ''


def p_id_number(p):
    '''IDNUM : ID
    | NUMBER'''
    global id_number
    if len(str(id_number)) > 0:
        id_number = str(id_number) + ',' + str(p[1])
    else:
        id_number = str(p[1])


# +++++++++++++++++++++/ ASSIGN OR UPDATE MANAGEMENT \++++++++++++++++++++++
'''
	E->E+-T; E->T; T->T*/F; T->F; F->id; F->(E)
'''


def p_S_ASSIGN(p):
    ''' S : VAMC ASSIGN UPDATE'''
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
        operands_stack.append('-' + p[1])
    else:
        print("Variable '" + p[1] + "' not declared yet")


# Productions F with sized variables
def p_F_array(p):
    '''F : ID SQBL IDNUM SQBR'''
    if p[1] in symbols:
        global id_number
        operands_stack.append('-' + p[1] + '[' + str(id_number) + ']')
        id_number = ''
    else:
        print("Variable '" + p[1] + "' not declared yet")


def p_F_matrix(p):
    '''F : ID SQBL IDNUM COMMA IDNUM SQBR'''
    if p[1] in symbols:
        global id_number
        operands_stack.append('-' + p[1] + '[' + str(id_number) + ']')
        id_number = ''
    else:
        print("Variable '" + p[1] + "' not declared yet")

def p_F_cube(p):
    '''F : ID SQBL IDNUM COMMA IDNUM COMMA IDNUM SQBR'''
    if p[1] in symbols:
        global id_number
        operands_stack.append('-' + p[1] + '[' + str(id_number) + ']')
        id_number = ''
    else:
        print("Variable '" + p[1] + "' not declared yet")


# F with a number value
def p_F_NUMBER(p):
    '''F : NUMBER'''
    operands_stack.append(p[1])


def p_FtoE(p):
    '''F : PARL CONDITION PARR'''


# To handle variables, array, matrix, cube assign function
def p_vamc(p):
    '''VAMC : ID'''
    operands_stack.append('-' + p[1])


def p_vamc_array(p):
    '''VAMC : ID SQBL IDNUM SQBR'''
    global id_number
    operands_stack.append('-' + p[1] + '[' + str(id_number) + ']')
    id_number = ''

def p_vamc_matrix(p):
    '''VAMC : ID SQBL IDNUM COMMA IDNUM SQBR'''
    global id_number
    operands_stack.append('-' + p[1] + '[' + str(id_number) + ']')
    id_number = ''

def p_vamc_cube(p):
    '''VAMC : ID SQBL IDNUM COMMA IDNUM COMMA IDNUM SQBR'''
    global id_number
    operands_stack.append('-' + p[1] + '[' + str(id_number) + ']')
    id_number = ''

# +++++++++++++++++++++/ IF MANAGEMENT \++++++++++++++++++++++
def p_S_IF(p):
    '''S : IF CONDITION AUXCOLON ST ENDIF'''
    global program_counter
    program_counter += 1
    program_instructions.append('Goto ' + str(program_counter))

    aux = go_to_f_position.pop()
    aux2 = program_instructions[aux].find(' - ')
    program_instructions[aux] = program_instructions[aux][0:aux2 + 1] + str(program_counter)


def p_S_IF2(p):
    '''S : IF CONDITION AUXCOLON ST ELSE COLON AUXQ ST AUXENDIF ENDIF'''


# AUX to adjust quadruple stack and insert the Goto after the true statements and to modify the go to false
def p_AUXQ(p):
    '''AUXQ : empty'''
    global program_counter
    program_counter += 1
    program_instructions.append('Goto ')
    first_instruction_condition.append(program_counter)

    aux = go_to_f_position.pop()
    aux2 = program_instructions[aux].find(' - ')
    program_instructions[aux] = program_instructions[aux][0:aux2 + 1] + str(program_counter)


def p_AUXENDIF(p):
    '''AUXENDIF : empty'''
    global program_counter
    program_counter += 1
    program_instructions.append('Goto ' + str(program_counter))

    aux = first_instruction_condition.pop()
    program_instructions[aux - 1] = 'Goto ' + str(program_counter)


# +++++++++++++++++++++/ WHILE MANAGEMENT \++++++++++++++++++++++
def p_S_WHILE(p):
    ''' S : WHILE AUXWHILE CONDITION AUXCOLON ST AUXENDWHILE ENDW'''


def p_AUXWHILE(p):
    '''AUXWHILE : empty'''
    first_instruction_condition.append(program_counter)


def p_AUXENDWHILE(p):
    '''AUXENDWHILE : empty'''
    global program_counter
    program_instructions.append('Goto ' + str(first_instruction_condition.pop()))
    program_counter += 1

    aux = go_to_f_position.pop()
    aux2 = program_instructions[aux].find(' - ')
    program_instructions[aux] = program_instructions[aux][0:aux2 + 1] + str(program_counter)


# +++++++++++++++++++++/ QUADRUPLES DEFINITION \++++++++++++++++++++++
# Quadruples stacks variables
operands_stack = deque()
execution_queue = []  # List to store quadruples
avail_temporales = deque(['T1'])
avail_aux = []  # Temporal in use
iAvail = 2  # Execution index


# Looking for existing avails
def existing_avail(value):
    try:
        avail_aux.index(value)
        avail_temporales.append(value)
        avail_aux.remove(value)
    except:
        pass


def quadruple_generation(operator):
    global iAvail
    execution_queue.append(operator)
    # Operands
    aux_operand = operands_stack.pop()
    execution_queue.append(operands_stack.pop())

    existing_avail(execution_queue[-1])  # Operand equal to a temporal

    execution_queue.append(aux_operand)

    existing_avail(execution_queue[-1])  # Operand equal to a temporal

    if operator != '=':
        operands_stack.append(avail_temporales.popleft())
        execution_queue.append(operands_stack[-1])
        avail_aux.append(operands_stack[-1])
        avail_temporales.append('T' + str(iAvail))  # New temporal
        iAvail += 1

    # print(execution_queue)

    global program_counter
    program_instructions.append(execution_queue[:])
    program_counter += 1

    execution_queue.clear()


# +++++++++++++++++++++/ CONDITION MANAGEMENT \++++++++++++++++++++++
first_instruction_condition = []
go_to_f_position = []


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
    global program_counter
    program_instructions.append("GotoF~" + str(program_instructions[-1][-1]) + " - ")
    go_to_f_position.append(program_counter)
    program_counter += 1


# ---------------------------------< END STATEMENTS >---------------------------------


def p_empty(p):
    ''' empty :	'''
    pass


# THROWING ERROR
def p_error(p):
    print("\tSyntax error in line " + str(p.lineno))


parser = yacc.yacc()
# f = open("codigoIntermedio2.txt", "r")
#f = open("recursion.txt", "r")
#f = open("suma_multiplicacion_mat", "r")
#f = open("sort_vector.txt", "r")
f = open("factorial.txt", "r")

parser.parse(f.read())
#print(symbols)
#print(program_instructions)
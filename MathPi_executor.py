from MathPi import program_instructions, symbols
import re
from collections import deque
# ---------------------------< QUADRUPLE MANAGEMENT >---------------------------

availValues = {}
operator = re.compile("\+|-|\*|\/")
comparator = re.compile(">|<|={2}?|!=|(AND){1}?|(OR){1}?")


# +++++++++++++++ / Comparation \ +++++++++++++++
def comparation(operation, operation_type):
    type = "BOOL"
    if operation[0] == '>':
        availValues[operation[3]] = [operation[1] > operation[2], type]
    elif operation[0] == '<':
        availValues[operation[3]] = [operation[1] < operation[2], type]
    elif operation[0] == '==':
        availValues[operation[3]] = [operation[1] == operation[2], type]
    elif operation[0] == 'OR':
        availValues[operation[3]] = [operation[1] or operation[2], type]
    elif operation[0] == 'AND':
        availValues[operation[3]] = [operation[1] and operation[2], type]
    else:
        availValues[operation[3]] = [operation[1] != operation[2], type]


# +++++++++++++++ / Sum, Substraction, Multiplication, Division \ +++++++++++++++
def ssmd(operation, operation_type):
    type = translate_type(operation_type)
    if operation[0] == '+':
        if type == 'INT':
            availValues[operation[3]] = [int(operation[1] + operation[2]), type]
        else:
            availValues[operation[3]] = [float("{:.2f}".format(operation[1] + operation[2])), type]
    elif operation[0] == '-':
        if type == 'INT':
            availValues[operation[3]] = [int(operation[1] - operation[2]), type]
        else:
            availValues[operation[3]] = [float("{:.2f}".format(operation[1] - operation[2])), type]
    elif operation[0] == '*':
        if type == 'INT':
            availValues[operation[3]] = [int(operation[1] * operation[2]), type]
        else:
            availValues[operation[3]] = [float("{:.2f}".format(operation[1] * operation[2])), type]
    else:
        if type == 'INT':
            availValues[operation[3]] = [int(operation[1] / operation[2]), type]
        else:
            availValues[operation[3]] = [float("{:.2f}".format(operation[1] / operation[2])), type]


# +++++++++++++++++++++/ Type Translation \++++++++++++++++++++++

def translate_type(operation_type):
    if operation_type[0] == 'INT' and operation_type[1] == 'INT':
        return 'INT'
    elif operation_type[0] == 'INT' and operation_type[1] == 'FLOAT':
        return 'FLOAT'
    elif operation_type[0] == 'FLOAT' and operation_type[1] == 'INT':
        return 'FLOAT'
    elif operation_type[0] == 'FLOAT' and operation_type[1] == 'FLOAt':
        return 'FLOAT'



# +++++++++++++++ / Does it have a value? \ +++++++++++++++
# +++++++++++++++ / Operation Formation \ +++++++++++++++
def hasValue(operand, operation, operation_type):

    if isinstance(operand, str) and operand[0] == '-':
        if symbols[operand[1:]][0] == "NULL":
            return False
        else:
            operation.append(symbols[operand[1:]][0])
            operation_type.append(symbols[operand[1:]][1])
    elif isinstance(operand, str):
        operation.append(availValues[operand][0])
        operation_type.append(availValues[operand][1])
    else:
        operation.append(operand)
        if isinstance(operand, int):
            operation_type.append('INT')
        elif isinstance(operand, float):
            operation_type.append('FLOAT')
    return True


# +++++++++++++++ / Classification  of operation \ +++++++++++++++
def manageQuadruples(q):
    value = True
    operation = []
    operation_type = []

    if operator.match(q[0]):
        operation.append(q[0])
        for i in (1, 2):
            if value:
                value = hasValue(q[i], operation, operation_type)
        operation.append(q[3])
        if value:
            ssmd(operation, operation_type)
        operation.clear()
        operation_type.clear()

    elif comparator.match(q[0]):
        operation.append(q[0])
        for i in (1, 2):
            if value:
                value = hasValue(q[i], operation, operation_type)
        operation.append(q[3])
        if value:
            comparation(operation, operation_type)
        operation.clear()
        operation_type.clear()

    else:  # Assign section
        operation.append(q[0])
        value = hasValue(q[2], operation, operation_type)
        operation.insert(1, q[1])
        if value:
            symbols[operation[1][1:]][0] = operation[2]
        operation.clear()
        operation_type.clear()
    return not value


# ---------------------------< END OF QUADRUPLE MANAGEMENT >---------------------------


# ---------------------------< READ EXECUTION >---------------------------

def inputExecution(q):
    if symbols[q][1] == 'INT':
        symbols[q][0] = int(input())
    elif symbols[q][1] == 'FLOAT':
        symbols[q][0] = float(input())

# ---------------------------< END OF READ EXECUTION >---------------------------


# ---------------------------< PRINT EXECUTION >---------------------------

def printExecution(q):
    try:
        print(symbols[q][0])
    except:
        print(q)

# ---------------------------< END OF PRINT EXECUTION >---------------------------

def main():
    error = False
    program_counter = 0
    aux_back_procedure = []

    print(program_instructions)

    while program_counter < len(program_instructions) and not error:
        if program_instructions[program_counter][0:4] == "Goto" and program_instructions[program_counter][0:5] != "GotoF":
            program_counter = int(program_instructions[program_counter][5:])
        elif program_instructions[program_counter][0:5] == "GotoF":
            aux = program_instructions[program_counter].find('~')
            aux2 = program_instructions[program_counter].find(' ')
            if not availValues[program_instructions[program_counter][aux + 1 : aux2]][0]:
                program_counter = int(program_instructions[program_counter][aux2+1:])
            else:
                program_counter += 1
            pass
        elif program_instructions[program_counter][0:5] == "GOSUB":
            aux_back_procedure.append(program_counter)
            program_counter = symbols[program_instructions[program_counter][6:]][0]
        elif program_instructions[program_counter] == 'END PROCEDURE':
            program_counter = aux_back_procedure.pop() + 1 # HAcerlo como lo tenia pero en vez de fila con stacks
        elif program_instructions[program_counter][0:5] == "INPUT":
            inputExecution(program_instructions[program_counter][6:])
            program_counter += 1
        elif program_instructions[program_counter][0] == 'PRINT':
            printExecution(program_instructions[program_counter][1])
            program_counter += 1
        else:
            error = manageQuadruples(program_instructions[program_counter])
            program_counter += 1

    print(symbols)
    if error:
        print("ERROR: VARIABLE HAS NOT BEEN INITIALIZED")


#

# print(program_instructions)
# print("Lenght of instructionss: " + str(len(program_instructions)))
# print(symbols)
# print(proceduresPos)


if __name__ == '__main__':
    main()

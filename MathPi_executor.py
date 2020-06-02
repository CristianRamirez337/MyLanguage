from MathPi import program_instructions, symbols
import re
from collections import deque

# ---------------------------< QUADRUPLE MANAGEMENT >---------------------------

avail_values = {}
operator = re.compile("\+|-|\*|\/")
comparator = re.compile(">|<|={2}?|!=|(AND){1}?|(OR){1}?")
sized_variables = []


# +++++++++++++++ / Comparation \ +++++++++++++++
def comparation(operation, operation_type):
    type = "BOOL"
    if operation[0] == '>':
        avail_values[operation[3]] = [operation[1] > operation[2], type]
    elif operation[0] == '<':
        avail_values[operation[3]] = [operation[1] < operation[2], type]
    elif operation[0] == '==':
        avail_values[operation[3]] = [operation[1] == operation[2], type]
    elif operation[0] == 'OR':
        avail_values[operation[3]] = [operation[1] or operation[2], type]
    elif operation[0] == 'AND':
        avail_values[operation[3]] = [operation[1] and operation[2], type]
    else:
        avail_values[operation[3]] = [operation[1] != operation[2], type]


# +++++++++++++++ / Sum, Substraction, Multiplication, Division \ +++++++++++++++
def ssmd(operation, operation_type):
    type = translate_type(operation_type)
    if operation[0] == '+':
        if type == 'INT':
            avail_values[operation[3]] = [int(operation[1] + operation[2]), type]
        else:
            avail_values[operation[3]] = [float("{:.2f}".format(operation[1] + operation[2])), type]
    elif operation[0] == '-':
        if type == 'INT':
            avail_values[operation[3]] = [int(operation[1] - operation[2]), type]
        else:
            avail_values[operation[3]] = [float("{:.2f}".format(operation[1] - operation[2])), type]
    elif operation[0] == '*':
        if type == 'INT':
            avail_values[operation[3]] = [int(operation[1] * operation[2]), type]
        else:
            avail_values[operation[3]] = [float("{:.2f}".format(operation[1] * operation[2])), type]
    else:
        if type == 'INT':
            avail_values[operation[3]] = [int(operation[1] / operation[2]), type]
        else:
            avail_values[operation[3]] = [float("{:.2f}".format(operation[1] / operation[2])), type]


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
        if not ('[' in operand) and symbols[operand[1:]][0] == "NULL":
            return False
        else:
            if operand.find('[') != -1:
                # Getting value from the memory array
                operation.append(sized_variables[sized_variables_manipulation(operand)])
                if 'INT' in symbols[operand[1:operand.find('[')]][1]:
                    operation_type.append('INT')
                else:
                    operation_type.append('FLOAT')
            else:
                operation.append(symbols[operand[1:]][0])
                operation_type.append(symbols[operand[1:]][1])
    elif isinstance(operand, str):
        operation.append(avail_values[operand][0])
        operation_type.append(avail_values[operand][1])
    else:
        operation.append(operand)
        if isinstance(operand, int):
            operation_type.append('INT')
        elif isinstance(operand, float):
            operation_type.append('FLOAT')
    return True


# +++++++++++++++ / Classification  of operation \ +++++++++++++++
def sized_variables_manipulation(operand):
    operand_sized = operand[operand.find('[') + 1: operand.find(']')].split(',')
    if operand_sized[0] in symbols.keys():
        operand_sized[0] = symbols[operand_sized[0]][0]
    if len(operand_sized) == 1:
        return int(operand_sized[0]) + int(symbols[operand[1:operand.find('[')]][0])
    elif len(operand_sized) == 2:
        if operand_sized[1] in symbols.keys():
            operand_sized[1] = symbols[operand_sized[1]][0]
        return int(operand_sized[0]) * int(symbols[operand[1:operand.find('[')]][2][1]) + int(
            operand_sized[1]) + int(symbols[operand[1:operand.find('[')]][0])
    else:
        if operand_sized[1] in symbols.keys():
            operand_sized[1] = symbols[operand_sized[1]][0]
        elif operand_sized[2] in symbols.keys():
            operand_sized[2] = symbols[operand_sized[2]][0]
        return int(operand_sized[0]) * int(symbols[operand[1:operand.find('[')]][2][2]) * \
               int(symbols[operand[1:operand.find('[')]][2][1]) + int(operand_sized[1]) \
               + int(operand_sized[1]) * int(symbols[operand[1:operand.find('[')]][2][2]) \
               + int(operand_sized[2]) + int(symbols[operand[1:operand.find('[')]][0])


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
            if '[' in str(operation[1]) and '[' in str(operation[2]):
                sized_variables[sized_variables_manipulation(operation[1])] = sized_variables[
                    sized_variables_manipulation(operation[2])]
            elif '[' in str(operation[1]) and not ('[' in str(operation[2])):
                sized_variables[sized_variables_manipulation(operation[1])] = operation[2]
            else:
                if '[' in str(operation[2]):
                    symbols[operation[1][1:]][0] = sized_variables[sized_variables_manipulation(operation[2])]
                else:
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
        # to_print = ''
        # for i in q:
        #     to_print = to_print + ' ' + str(symbols[i][0])
        # print(to_print)
    except:
        print(q)


# ---------------------------< END OF PRINT EXECUTION >---------------------------

def main():
    error = False
    program_counter = 0
    aux_back_procedure = []
    base = 0

    program_counter_register = []

    #print(program_instructions)
    for i in symbols:
        if 'ARRAY' in symbols[i][1]:
            symbols[i][0] = base
            base += symbols[i][2]
        elif 'MATRIX' in symbols[i][1]:
            symbols[i][0] = base
            base += (symbols[i][2][0]) * (symbols[i][2][1])
        elif 'CUBE' in symbols[i][1]:
            symbols[i][0] = base
            base += (symbols[i][2][0]) * (symbols[i][2][1]) * (symbols[i][2][2])

    global sized_variables
    sized_variables = [0] * base

    while program_counter < len(program_instructions) and not error:
        program_counter_register.append(program_counter)
        if program_instructions[program_counter][0:4] == "Goto" and program_instructions[program_counter][
                                                                    0:5] != "GotoF":
            program_counter = int(program_instructions[program_counter][5:])
        elif program_instructions[program_counter][0:5] == "GotoF":
            aux = program_instructions[program_counter].find('~')
            aux2 = program_instructions[program_counter].find(' ')
            if not avail_values[program_instructions[program_counter][aux + 1: aux2]][0]:
                program_counter = int(program_instructions[program_counter][aux2 + 1:])
            else:
                program_counter += 1
            pass
        elif program_instructions[program_counter][0:5] == "GOSUB":
            aux_back_procedure.append(program_counter)
            program_counter = symbols[program_instructions[program_counter][6:]][0]
        elif program_instructions[program_counter] == 'END PROCEDURE':
            program_counter = aux_back_procedure.pop() + 1  # HAcerlo como lo tenia pero en vez de fila con stacks
        elif program_instructions[program_counter][0:5] == "INPUT":
            inputExecution(program_instructions[program_counter][6:])
            program_counter += 1
        elif program_instructions[program_counter][0] == 'PRINT':
            printExecution(program_instructions[program_counter][1])
            program_counter += 1
        else:
            error = manageQuadruples(program_instructions[program_counter])
            program_counter += 1

    #print(symbols)
    #print(sized_variables)
    if error:
        print("ERROR: VARIABLE HAS NOT BEEN INITIALIZED")


#

# print(program_instructions)
# print("Lenght of instructionss: " + str(len(program_instructions)))
# print(symbols)
# print(proceduresPos)


if __name__ == '__main__':
    main()

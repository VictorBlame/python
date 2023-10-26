import sys

operators = ('+', '-', '*', '/')


def calculator(num1, operator, num2):
    if operator == operators[0]:
        return int(num1) + int(num2)
    elif operator == operators[1]:
        return int(num1) - int(num2)
    elif operator == operators[2]:
        return int(num1) * int(num2)
    elif operator == operators[3]:
        return int(num1) / int(num2)
    else:
        raise NotImplementedError('Operation is not implemented')


if len(sys.argv) != 4:
    raise SyntaxError('Argument number error. Argument template is: fileName number1 operator number2')


result = calculator(sys.argv[1], sys.argv[2], sys.argv[3])
print('The result of the calculation is: ' + str(result))
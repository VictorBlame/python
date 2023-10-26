import argparse

parser = argparse.ArgumentParser()
parser.add_argument('number', metavar='N', type=int, help='decimal number')
arguments = parser.parse_args()


def sum_binary_1(decimal):
    try:
        binary = format(decimal, "b")
        counter = 0
        for digit in binary:
            if int(digit) == 1:
                counter += 1
        print('- n = ' + str(decimal) + ' = ' + str(binary) + ' result = ' + str(counter))
        return counter
    except:
        return None


sum_binary_1(arguments.number)

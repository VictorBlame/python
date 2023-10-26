def eligibleForVote(age):
    if age < 0:
        print('Invalid age')
    elif age >= 18:
        print('Eligible')
    else:
        print('Not eligible')


def evenOrOdd(number):
    even = True if number % 2 == 0 else False
    if even:
        print('Even')
    else:
        print('Odd')


def grade(score):
    if 90 <= score <= 100:
        print('5')
    elif 80 <= score <= 89:
        print('4')
    elif 65 <= score <= 79:
        print('3')
    elif 50 <= score <= 64:
        print('2')
    elif 0 <= score <= 49:
        print('1')
    else:
        print('Invalid score')


def count():
    for number in range(1, 11):
        print(number)


def triangle(firstLine):
    for row in range(len(firstLine) + 1, 0, -1):
        for step in range(1, row):
            print('*', end='')
        print('\r')


def xCounter(string):
    count = 0
    for item in range(0, len(string)):
        if string[item] == 'x':
            count += 1
    print(count)


def xRemover(string):
    hasX = False
    for item in range(0, len(string)):
        if string[item] == 'x':
            hasX = True
    if hasX:
        print(string.replace('x', ''))
    else:
        print('No x character was found')


def reverseString(string):
    print(string[::-1])


def doubleString(string):
    doubledArray = ''
    for char in string:
        doubledArray += 2*char
    print(doubledArray)


def divisible3():
    counter = 0
    for number in range(1, 1001):
        if number % 3 == 0:
            counter += 1
            print(number)
    print('Divisible numbers by 3 between 1-1000: ' + str(counter))


print('Task 1')
eligibleForVote(26)
print('Task 2')
evenOrOdd(-1)
print('Task 3')
grade(0)
print('Task 4')
count()
print('Task 5')
triangle('*******')
print('Task 6')
xCounter('xixoxixoxo')
print('Task 7')
xRemover('ahahahahahahahahxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxahahahahahahhaxffff')
print('Task 8')
reverseString('Elment vadászni a QA bugokra!+/*@')
print('Task 9')
doubleString('cica')
print('Task 10')
divisible3()
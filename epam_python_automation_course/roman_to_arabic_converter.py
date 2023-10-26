import argparse

parser = argparse.ArgumentParser()
parser.add_argument('roman_number', metavar='R', type=str, help='roman number')
arguments = parser.parse_args()

roman_arabic_dictionary = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000
}


arabic_roman_dictionary = {
    '1000': 'M',
    '500': 'D',
    '100': 'C',
    '50': 'L',
    '10': 'X',
    '5': 'V',
    '1': 'I'
}


def roman_arabic_converter(roman):
    values = []
    for letter in roman:
        values.append(roman_arabic_dictionary[letter])
    for item in range(3, len(values)):
        if values[item] == values[item - 1] == values[item - 2] == values[item - 3]:
            raise ValueError('Maximum 3 characters can be the same next to each other')
    for value in range(0, len(values)):
        if value < len(values) - 1:
            if values[value] < values[value + 1]:
                values[value] *= -1
    print(str(roman) + ' --> ' + str(sum(values))) if sum(values) < 4000 else print('MMMCMXCIX (arabic 3999) is the biggest number')


def arabic_roman_converter(arabic):
    template = 'MDCLXVI'
    roman = ''
    arabic_normalized = []
    if int(arabic) > 3999 or int(arabic) < 1:
        raise ValueError('Numbers only acceptable between 1 and  3999')
    else:
        arabic_normalized.append(arabic_roman_dictionary['1000'] * arabic[0])
        print(str(arabic_normalized))


#for i in arguments.roman_number:
#    if i not in roman_arabic_dictionary:
#        raise ValueError('Character is not in the dictionary')

arabic_roman_converter(arguments.roman_number)

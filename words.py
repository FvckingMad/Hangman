from random import choice

file = open('data/words.txt', encoding='UTF-8')
words = [line.strip() for line in file.readlines()]


def get_words():
    data = words
    word_str = choice(data)

    word_arr = []
    showing_word = ''

    for letter in word_str:
        if letter in (word_str[0], word_str[-1]):
            showing_word += letter
        else:
            showing_word += '_'

        showing_word += ' '
        word_arr.append(letter)

    return word_arr, showing_word.split()

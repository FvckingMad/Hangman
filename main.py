from tkinter import CENTER, Tk, Label, Button, Canvas, Event
from turtle import RawTurtle, TurtleScreen

from words import get_words
from drawings import drawing_stages, erase
from consts import (
    MAIN_WINDOW_SIZE, MAIN_WINDOW_TITLE, WIDTH, HEIGHT, GALLOWS_WINDOW_WIDTH,
    GALLOWS_WINDOW_HEIGHT, GALLOWS_WINDOW_PAD_Y, GALLOWS_WINDOW_COLOR_MODE,
    GALLOWS_WINDOW_BACKGROUND_COLOR, PENCIL_SIZE, PENCIL_SPEED, ERASER_SIZE,
    ERASER_SPEED, ERASER_SHAPE, ERASER_COLOR, FONT_WORD, WORD_LABEL_PAD_Y,
    RESULT_WINDOW_REL_X, RESULT_WINDOW_REL_Y, FONT_RESULT, RIGHT_BUTTON_COLOR,
    VICTORY_LABEL_TEXT, VICTORY_LABEL_COLOR, WRONG_BUTTON_COLOR, BUTTON_SIZE,
    DEFEAT_LABEL_TEXT, DEFEAT_LABEL_COLOR, LETTERS, BINDS, FONT_BUTTON,
    KEYBOARD_FIRST_ROW_X, KEYBOARD_FIRST_ROW_Y, KEYBOARD_SECOND_ROW_X,
    KEYBOARD_SECOND_ROW_Y, KEYBOARD_THIRD_ROW_X, KEYBOARD_THIRD_ROW_Y,
    BUTTONS_DISTANCE_X, DEFAULT_BUTTON_COLOR)
from sounds import (SOUND_GUESSED, SOUND_FAILED, SOUND_NONE,
                    SOUND_VICTORY, SOUND_DEFEAT, SOUND_PENCIL,
                    SOUND_ERASER)


# Создание главного окна игры
window = Tk()
window.geometry(MAIN_WINDOW_SIZE)
window.title(MAIN_WINDOW_TITLE)
window.resizable(width=WIDTH, height=HEIGHT)


# Создание окна с виселицей
canvas = Canvas(master=window,
                width=GALLOWS_WINDOW_WIDTH,
                height=GALLOWS_WINDOW_HEIGHT)
canvas.pack(pady=GALLOWS_WINDOW_PAD_Y)

gallows = TurtleScreen(canvas)
gallows.colormode(GALLOWS_WINDOW_COLOR_MODE)
gallows.bgcolor(GALLOWS_WINDOW_BACKGROUND_COLOR)


# Создание инструментов для рисования
pencil = RawTurtle(gallows)
pencil.hideturtle()
pencil.pensize(PENCIL_SIZE)
pencil.speed(PENCIL_SPEED)

eraser = RawTurtle(gallows)
eraser.pensize(ERASER_SIZE)
eraser.speed(ERASER_SPEED)
eraser.shape(ERASER_SHAPE)
eraser.color(ERASER_COLOR)


# Объявление переменных для игры
def prepare():
    global word
    global word_show
    global word_label
    global result_label
    global stack
    global count_wrong_letters

    word, word_show = get_words()
    word_label = Label(window, text=word_show, font=FONT_WORD)
    word_label.pack(pady=WORD_LABEL_PAD_Y)

    result_label = Label(window)
    result_label.place(relx=RESULT_WINDOW_REL_X,
                       rely=RESULT_WINDOW_REL_Y,
                       anchor=CENTER)

    stack = []
    count_wrong_letters = 0

    return (word, word_show, word_label,
            result_label, stack, count_wrong_letters)


(word, word_show, word_label,
 result_label, stack, count_wrong_letters) = prepare()


# Правильная кнопка
def right_letter(button):
    SOUND_GUESSED.play()
    button.configure(background=RIGHT_BUTTON_COLOR)

    for i in range(len(word)):
        if word[i] == button['text']:
            word_show[i] = button['text']

    word_label.configure(text=word_show)

    if '_' not in word_show:
        result_label.configure(text=VICTORY_LABEL_TEXT,
                               font=FONT_RESULT,
                               foreground=VICTORY_LABEL_COLOR)

        result_label.update()

        SOUND_VICTORY.play()
        window.after(2000, start_game)
    else:
        keyboard('ACTIVATE')


# Неправильная буква
def wrong_letter(button):
    global count_wrong_letters
    global word_show

    SOUND_FAILED.play()
    button.configure(background=WRONG_BUTTON_COLOR)
    SOUND_PENCIL.play(maxtime=drawing_stages[count_wrong_letters][1])
    drawing_stages[count_wrong_letters][0](pencil)

    count_wrong_letters += 1

    if count_wrong_letters >= len(drawing_stages):
        window.after(1000)
        word_show = word

        result_label.configure(text=DEFEAT_LABEL_TEXT,
                               font=FONT_RESULT,
                               foreground=DEFEAT_LABEL_COLOR)
        result_label.update()

        word_label.configure(text=word_show)

        SOUND_DEFEAT.play()
        window.after(2500, start_game)
    else:
        keyboard('ACTIVATE')


buttons = []


# Обновление клавиатуры
def keyboard(mode):
    if mode == 'DISABLE':
        for button_number in range(len(BINDS)):
            buttons[button_number].configure(state='disabled')
            window.unbind(BINDS[button_number])

    elif mode == 'ACTIVATE':
        for button_number in range(len(BINDS)):
            buttons[button_number].configure(state='normal')
            window.bind(BINDS[button_number], click)

    elif mode == 'REFRESH':
        for button_number in range(len(BINDS)):
            buttons[button_number].configure(background=DEFAULT_BUTTON_COLOR)
            window.bind(BINDS[button_number], click)


# Обработка нажатия на клавишу
def click(button: any):
    global count_wrong_letters

    if isinstance(button, Event):
        letter = LETTERS[BINDS.index(button.char)]
        button = buttons[BINDS.index(button.char)]
    else:
        letter = button['text']

    button.configure(relief='sunken')
    button.configure(background=DEFAULT_BUTTON_COLOR)
    button.update()
    button.after(100, button.configure(relief='raised'))

    if letter in stack:
        SOUND_NONE.play()

        if letter in word:
            button.configure(background=RIGHT_BUTTON_COLOR)
        else:
            button.configure(background=WRONG_BUTTON_COLOR)

    else:
        keyboard('DISABLE')
        stack.append(letter)

        if letter in word:
            right_letter(button)
        else:
            wrong_letter(button)


# Создание клавиатуры
letter_number = 0
x, y = KEYBOARD_FIRST_ROW_X, KEYBOARD_FIRST_ROW_Y

while letter_number != len(LETTERS):
    button_name = f'button_{letter_number + 1}'

    creating_button_command = (
        f'''{button_name} = {Button.__name__}(
        text='{LETTERS[letter_number]}',
        background='{DEFAULT_BUTTON_COLOR}',
        command=lambda: click({button_name}),
        font={FONT_BUTTON})''')

    placing_button_command = (
        f'''{button_name}.place(
        x={x}, y={y},
        width={BUTTON_SIZE}, height={BUTTON_SIZE})''')

    appending_button_command = f'buttons.append({button_name})'

    binding_button_command = f'window.bind("{BINDS[letter_number]}", click)'

    exec(creating_button_command)
    exec(placing_button_command)
    exec(appending_button_command)
    exec(binding_button_command)

    x += BUTTONS_DISTANCE_X

    if LETTERS[letter_number] == 'Ъ':
        x, y = KEYBOARD_SECOND_ROW_X, KEYBOARD_SECOND_ROW_Y

    if LETTERS[letter_number] == 'Э':
        x, y = KEYBOARD_THIRD_ROW_X, KEYBOARD_THIRD_ROW_Y

    letter_number += 1


# Начало игры
def start_game():
    word_label.destroy()
    result_label.destroy()
    keyboard('REFRESH')

    if count_wrong_letters > 0:
        SOUND_ERASER.play()
        erase(eraser)
        window.after(1300)
        SOUND_ERASER.stop()
    prepare()
    keyboard('ACTIVATE')


window.mainloop()

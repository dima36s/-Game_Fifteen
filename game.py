from random import shuffle
from tkinter import Canvas, Tk

board_size = 2
square_size = 80
empty_square = board_size ** 2

root = Tk()
root.title("Fifteen")

draw = Canvas(root, width=board_size * square_size,
              height=board_size * square_size, bg='green')
draw.pack()


def get_count():  # Функция считающая количество перемещений

    inversions = 0
    inversion_board = board[:]
    inversion_board.remove(empty_square)
    for i in range(len(inversion_board)):
        first_item = inversion_board[i]
        for j in range(i + 1, len(inversion_board)):
            second_item = inversion_board[j]
            if first_item > second_item:
                inversions += 1
    return inversions


def is_solvable():  # Проверка, есть ли решение головоломки
    num_inversions = get_count()
    if board_size % 2 != 0:
        return num_inversions % 2 == 0
    else:
        empty_square_row = board_size - (board.index(empty_square) // board_size)
        if empty_square_row % 2 == 0:
            return num_inversions % 2 != 0
        else:
            return num_inversions % 2 == 0


def get_empty_neighbor(index):
    empty_index = board.index(empty_square)
    abs_value = abs(empty_index - index)
    if abs_value == board_size:
        return empty_index
    elif abs_value == 1:
        max_index = max(index, empty_index)
        if max_index % board_size != 0:
            return empty_index
    return index


def draw_board():  # Отрисовка игрового поля
    draw.delete('all')
    for i in range(board_size):
        for j in range(board_size):
            index = str(board[board_size * i + j])
            if index != str(empty_square):
                draw.create_rectangle(j * square_size, i * square_size,
                                      j * square_size + square_size,
                                      i * square_size + square_size,
                                      fill='#43ABC9',
                                      outline='#FFFFFF')
                draw.create_text(j * square_size + square_size / 2,
                                 i * square_size + square_size / 2,
                                 text=index,
                                 fill='#FFFFFF')


def show_victory_text():  # Рисуем черный квадрат по центру поля
    draw.create_rectangle(square_size / 5,
                          square_size * board_size / 2 - 10 * board_size,
                          board_size * square_size - square_size / 5,
                          square_size * board_size / 2 + 10 * board_size,
                          fill='#000000',
                          outline='#FFFFFF')
    draw.create_text(square_size * board_size / 2, square_size * board_size / 1.9,
                     text="VICTORY!", fill='pink')


def click(event):  # Получаем координаты клика

    x, y = event.x, event.y
    x = x // square_size
    y = y // square_size
    board_index = x + (y * board_size)
    empty_index = get_empty_neighbor(board_index)
    board[board_index], board[empty_index] = board[empty_index], board[board_index]
    draw_board()
    if board == correct_board:
        show_victory_text()


draw.bind('<Button-1>', click)
draw.pack()

board = list(range(1, empty_square + 1))
correct_board = board[:]
shuffle(board)

while not is_solvable():
    shuffle(board)

draw_board()
root.mainloop()

"""
        Краткое описание игры Крестики-Нолики.
В начале вводятся входные параметры: цвета для игроков и необходимость отображения номеров клеток.
Далее начинает игрок "Х". После игрок "О", и т.д. Чей ход показывает программа.
Игрок может ввести одну цифру, тогда это номер клетки от 1 до 9, либо координаты из двух цифр от 1 до 3.

free_cells: основной список, куда записываются ходы игроков "X" и "O" под индексом номера клетки. Индекс 0 - клетка № 1.
        В начале игры в список помещаются номера клеток [1,2,3,..,7,8,9], после хода игрока "Х"
        например в клетку "2", список будет [1,"X",3,..,7,8,9] и т.д. Цифры будут переписаны "Х" и "О".
        В случае выбора игры без отображения номеров клеток (параметр 'show_cells'), вместо цифр ставятся пробел (" ").
Отображение игрового поля идет по списку free_cells, в зависимости от индекса.
Отображение номера клетки блеклым светлым цветом.
Отображение игроков "Х" и "О" на поле жирным шрифтом, по цветам в зависимости от входных параметров "options",
полученных в начале программы (Пример: {'color_X': 5, 'color_O': 6, 'show_cells': False, 'cells_wins': {0, 1, 2}}).
Параметр 'cells_wins': {0, 1, 2} - отображает список "победных" клеток, которым назначается стиль "Мерцание".

Некоторые места в программе можно было сделать проще.
Например, использование генератора gen_row_cells, который просто последовательно выдает по 3 значения
 из списка free_cells. Проще было сделать копию этого списка, и удалять из него по три элемента,
 перезаписывая список:
                        new_free_cells = free_cells.copy()
          В теле цикла: row = new_free_cells[:3]
                        s = s.format(*row)
                        new_free_cells = new_free_cells[3:]

Эти упрощения не делались намеренно мной, хотелось применить полученные навыки из материалов обучения,
важных таких как генераторы, декораторы, all, any, map, list comprehension, тернарный оператор, ... )
"""


def gen_row_cells(free_cells: list) -> list:
    """
    Генератор выдачи по три ячейки для игрового поля из основного списка free_cells.
    :param free_cells: list.
        Основной список ходов игроков. Например: [1,'O','X',4,'X',6,'O','X',9]
        или [' ','O','X',' ','X',' ','O','X',' '] если вывод поля, без отображения номеров клеток.
    :return yield row: list.
        Отдача по (для) одной строки. При первом обращении отдаст:
            [1,'O','X'] или [' ','O','X'], потом:
            [4,'X',6,] или [' ','X',' '], потом:
            ['O','X',9] или ['O','X',' ']
    """
    cells = free_cells.copy()
    while True:
        row = cells[:3]
        yield row
        cells = cells[3:]
        if not len(cells):
            break


def change_char(char: str, ch_options: dict) -> str:
    """
    Изменение цвета и атрибута символа или текста.
    :param char: str.
        Символ или строка, у которой надо поменять цвет, или стиль.
    :param ch_options: dict:
        'color': int.
            Цвет, на который надо поменять. Формат вставки "\033[{код цвета или стиля}m"
                Чёрный 30 (Фон 40)
                Красный 31 (Фон 41)
                Зелёный 32 (Фон 42)
                Жёлтый 33 (Фон 43)
                Синий 34 (Фон 44)
                Фиолетовый 35 (Фон 45)
                Бирюзовый 36 (Фон 46)
                Белый 37 (Фон 47)
        'style': list
            Стиль, на который поменять. Список чисел для стиля:
                0 Сброс к начальным значениям
                1 Жирный
                2 Блёклый
                3 Курсив
                4 Подчёркнутый
                5 Редкое мигание
                6 Частое мигание
                7 Смена цвета фона с цветом текста.
    :return: char: str.
        Символ или строка в новом цвете и стиле. Например "\033[1m\033[34mМОЙ_ТЕКСТ\033[0m" - для текста "МОЙ_ТЕКСТ"
    """
    char = f"\033[{ch_options['color'] + 30}m{char}\033[0m"  # Добавляем + 30, код цвета начинается с 30
    for s in ch_options['style']:  # Добавляем стили
        char = f"\033[{s}m" + char
    return char


def color_free_cells(func):
    """
    Декоратор. Изменение цвета значков для игрового поля.
    :param func:
    Принимает из функции (args[0]) основной список значений игрового поля вида [1,'O','X',4,'X',6,'O','X',9].
    Из kwargs: 'color_X' - цвет для значка "Х", 'color_O' - цвет для значка "О".
    Для цифр игрового поля, т.е. пустых клеток (номер клетки) задается Блёклый белый цвет.
    При победе одного из игрока в kwargs появляется ключ 'cells_wins', где лежат номера "победных" клеток.
    "Победным" клеткам добавляется мерцание.
    :return: func: с измененным "цветным" списком значений игрового поля.
    """
    def wrapper(*args, **kwargs):
        cells = args[0]  # Чтение списка значений клеток
        new_cells = []  # Новый список цветных значений
        # print(f" Параметры 'options' (kwargs): {kwargs}")

        for ch in cells:  # Для каждой клетки меняем цвет и стиль
            if ch == 'X':
                color = kwargs['color_X']
                ch = change_char(ch, {'color': color, 'style': [1]})
            elif ch == 'O':
                color = kwargs['color_O']
                ch = change_char(ch, {'color': color, 'style': [1]})
            else:
                ch = change_char(ch, {'color': 7, 'style': [2, 3]})  # Для пустых клеток.
            new_cells.append(ch)

        if kwargs.get('cells_wins'):  # Если кто-то выиграл.
            cells_wins = kwargs.get('cells_wins')
            for i in cells_wins:  # Для каждой такой клетки
                ch = new_cells[i]
                ch = change_char(ch, {'color': 0, 'style': [5]})  # Добавляем мерцание
                new_cells[i] = ch

        args = new_cells
        return func(args, **kwargs)
    return wrapper


@color_free_cells
def show_fields(free_cells: list, **kwargs: dict) -> None:
    """
    Отображение игрового поля
    :param free_cells: Список значений полей
    :param kwargs: Параметры "options", полученных в начале программы.
     (Пример: {'color_X': 5, 'color_O': 6, 'show_cells': False, 'cells_wins': {0, 1, 2}})
     Параметр 'cells_wins': {0, 1, 2} формируется в момент выигрыша.
     kwargs - в самой функции не используется, необходим для декоратора, для придания цвета значков "Х" "О".
    :return:
    """
    print('\n ↓x\y→', end=' ')
    print('1' + ' ' * 3 + '2' + ' ' * 3 + '3')

    top_1 = (' ' * 5 + '┌───┬───┬───┐\n' + '  1  ')
    middle_1 = ('│' + ' {} ') * 3  # В эти строки будем подставлять "Х", "О" или номер клетки, или пустоту.
    bottom_1 = ('│\n' + ' ' * 5 + '├───┼───┼───┤\n' + '  2  ')

    middle_2 = ('│' + ' {} ') * 3  # В эти строки будем подставлять "Х", "О" или номер клетки, или пустоту.
    bottom_2 = ('│\n' + ' ' * 5 + '├───┼───┼───┤\n' + '  3  ')

    middle_3 = ('│' + ' {} ') * 3  # В эти строки будем подставлять "Х", "О" или номер клетки, или пустоту.
    bottom_3 = ('│\n' + ' ' * 5 + '└───┴───┴───┘\n')

    lst = [top_1, middle_1, bottom_1, middle_2, bottom_2, middle_3, bottom_3]

    gen_row = iter(gen_row_cells(free_cells))  # Генератор 3-х значений из списка [[1,2,3], [4.. ]
    # new_free_cells = free_cells.copy()  # В случае не использования генератора gen_row

    for string_id, s in enumerate(lst):
        if string_id % 2:  # Строки (нечетные) куда необходимо подставить значения из списка free_cells
            s = s.format(*next(gen_row))
            # В случае не использования генератора gen_row:
            # row = new_free_cells[:3]
            # s = s.format(*row)
            # new_free_cells = new_free_cells[3:]
        print(s, end='')


def cell_calculation(xy: list) -> int:
    """Вычисление клетки по координатом (x,y)
    :param xy: list. Координаты из двух цифр
    :return: cell: int. Номер клетки
    """
    cell = xy[1]
    if xy[0] == 2:
        cell = xy[1] + 3
    elif xy[0] == 3:
        cell = xy[1] + 6
    return cell


def users_input(user: str, fr_cell: list) -> int:
    """
    Ввод данных пользователем номера клетки или координаты клетки.
    :param user: "Х" или "О"
    :param fr_cell: Основной список клеток, где помечены ходы пользователя и пустые клетки.
    :return: cell: int. Номер клетки (1-9), куда сходил игрок.
    """
    while True:
        cell = 0
        place = input(f"\tХодит: {user}\n\nВведите номер клетки (1-9) или координаты 'x' 'y': ").split()

        if not all(p.isdigit() for p in place):
            print("\nНе число!!!\n")
            continue

        if len(place) == 1:
            cell = int(place[0])
            if not (0 < cell <= 9):
                print("\nВышли из диапазона (от 1 до 9)!!!\n")
                continue
        elif len(place) == 2:
            x, y = map(int, place)
            if not (0 < x <= 3 and 0 < y <= 3):
                print("\nВышли из диапазона координат (от 1 до 3)!!!\n")
                continue
            cell = cell_calculation([x, y])
        else:
            print("\nВведите одно или два числа!!!\n")
            continue

        if fr_cell[cell-1] == 'X' or fr_cell[cell-1] == 'O':
            print("\nКлетка занята!!!\n")
            continue
        break
    return cell


def win_position(user: str, cells: list, **kwargs) -> bool:
    """
     Проверка комбинаций на выигрыш.
    :param user: str. Игрок "Х" или "О"
    :param cells: list. Основной список клеток, где помечены ходы пользователя и пустые клетки.
    :param kwargs: 'cells_wins'. Набор "победных" клеток.
    :return: bool. Есть выигрыш или нет.
    """
    positions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    user_steps = set([i for i, x in enumerate(cells) if x == user])  # Ходы игрока "X" или "O"

    for p in positions:
        match_set = user_steps.intersection(set(p))  # Набор совпадений ходов и выигрышных позиций
        if len(match_set) == 3:
            kwargs['cells_wins'] = match_set  # передаем выигрышный набор в прорисовку игрового поля
            show_fields(cells, **kwargs)
            return True
    return False


def start(**kwargs):
    """
    Основная логика программы.
    :param kwargs: Входные параметры для игры:
        'color_X': Цвет игрока "Х",
        'color_O': Цвет игрока "О",
        'show_cells': Показывать или нет номера клеток на игровом поле})
    :return:
    """
    free_cells = (list(range(1, 10)) if kwargs['show_cells'] else [' ']*9)  # основной список игрового поля
    while True:
        step_count = free_cells.count('X') + free_cells.count('O')  # Кол-во ходов
        user = 'O' if step_count % 2 else 'X'  # Определяем пользователя, чей ход
        show_fields(free_cells, **kwargs)  # Рисуем игровое поле

        if step_count < 9:
            cell = users_input(user, free_cells)
            free_cells[cell-1] = user  # Помечаем выбранное поле пользователем ('X' или 'O') в списке клеток.
        elif step_count == 9:
            print(change_char(f"     --- Ничья --- \n", {'color': 7, 'style': [5]}))
            break

        if win_position(user, free_cells, **kwargs):
            color = kwargs['color_'+user]
            print(change_char(f"   === Выиграл {user} === \n", {'color': color, 'style': [1, 5]}))
            break


if __name__ == '__main__':
    """  Игра крестики нолики. Ввод параметров для игры. """

    colors = [" 1. Чёрный", " 2. Красный", " 3. Зелёный", " 4. Жёлтый", " 5. Синий (по умолчанию 'X')",
              " 6. Фиолетовый", " 7. Бирюзовый (по умолчанию 'O')", " 8. Белый"]

    print("\n Чтобы оставить по умолчанию нажмите Enter\n")
    for i, c in enumerate(colors):
        c = change_char(c, {'color': i, 'style': []})  # Изменение цвета текста (Для черного цвета код 30)
        print(c)

    color_X = input(f"\n Выберите цвет игрока 'X': ")
    color_O = input(f" Выберите цвет игрока 'O': ")

    color_X = (int(color_X)-1 if color_X.isdigit() and (0 < int(color_X) <= 8) else 4)
    color_O = (int(color_O)-1 if color_O.isdigit() and (0 < int(color_O) <= 8) else 6)

    show_cells = input(f"\n Показывать номера клеток? (по умолчанию ДА, для изменения введите любой символ) ")
    show_cells = (False if show_cells else True)

    options = {'color_X': color_X, 'color_O': color_O, 'show_cells': show_cells}

    start(**options)



# ===============================================================
# kwargs=== {'color_X': 4, 'color_O': 6, 'show_cells': '', 'cells_wins': {8, 2, 5}}
# kwargs - основной словарь, где хранится конфигурация игры и выигрышные ячейки
# ===============================================================
# if cell not in fr_cell:
    # print('===kwargs====', kwargs['show_cells'], kwargs)
# show_fields(user, free_cells, **kwargs)  # Рисуем игровое поле

# ----------------------------------------------------------
# ----------------------------------------------------------
# if user == 'X':
#     kwargs['style'] = [1, 5]  #
# kwargs[]
# color = kwargs['color_X']
# ch = change_char(ch, {'color': color, 'style': [1]})
# print("\033[3m\033[5m\033[33m     --- Ничья --- \033[0m\n")
# print(f"\033[5m\033[33m   === Выиграл {user} === \033[0m\n")
# print(change_char(f"   === Выиграл {user} === ", {'color': 7, 'style': [1, 5]}))

# ----------------------------------------------------------
# print(f"\nКлетка {cell} fr_cell= {fr_cell}!!!\n")
# ch = f'\033[1m\033[34m{i}\033[0m'
# print("===kwargs['cells_wins']=== ", kwargs['cells_wins'])
# print("===new_cells=== ", new_cells)    # Продолжить здесь!!!!
    # print(type(show_cells))
    # if show_cells:
    #     show_cells = True

    # print(f'----{color_X}-----{color_O} ==== {show_cells}')
# ----------------------------------------------------------
    # char = 'X'
    # option = {'color': 36, 'style': [1, 7]}
    # {30:'\033[30m', 31:' \033[31m'}
# ----------------------------------------------------------
# def users_input(user: str, fr_cell: list):
#     while True:
#         cell = 0
#         place = input(f"\tХодит: {user}\n\nВведите номер клетки (1-9) или координаты (x y): ").split()
#
#         if len(place) == 1:
#             if place[0].isdigit():
#                 cell = int(place[0])
#                 if not (0 < cell <= 9):
#                     print("Вышли из диапазона (от 1 до 9)\n")
#                     continue
#             else:
#                 print("Введите число\n")
#                 continue
#         elif len(place) == 2:
#             if place[0].isdigit() and place[1].isdigit():
#                 x, y = map(int, place)
#                 if not (0 < x <= 3 and 0 < y <= 3):
#                     print("Вышли из диапазона координат (от 1 до 3)\n")
#                     continue
#                 cell = cell_calculation([x, y])
#             else:
#                 print("Введите числа\n")
#                 continue
#         else:
#             print("Введите одно или два числа\n")
#             continue
#
#         if cell not in fr_cell:
#             print("Клетка занята\n")
#             continue
#         break
#     return cell
# ----------------------------------------------------------
    # cell = None  # Номер клетки (от 1 до 9) в игровом поле"
# print(f'Свободные: {free_cells}\n')
# print('Сумма ходов : ', step_count)
# ----------------------------------------------------------
# field = (user, cell)  # Поле - кортеж из user (X или O) и номер клетки (от 1 до 9)
# ---------------------------------------------------
    #         print('i=====: ', i)
    #     s = s.format(*free_cell[0:4])
    #         print('Treee c: ', next(gen_row))
    #         s = s.format()
    # print('free_cells = ', free_cell)
    # print('Treee c: ', next(gen_row))
    # for i in len(lst):
    #     if i == middle_1:
    #         x = 'W'
    #     elif i == middle_2:
    #         x = 'Z'
    #     print(i, end='')
    #
    # return True
# ------------------------------------------------------
    # if user == 'X':
    #     x = f'\033[1m\033[34m{user}\033[0m'
    # elif user == 'O':
    #     x = f'\033[1m\033[36m{user}\033[0m'
    # else:
    #     x = '\u2087'
    #     x = 7
    #     x = f'\033[2m\033[3m\033[37m{x}\033[0m'
# ---------------------------------------------------------
#     top_1 = (' ' * 5 + '┌───┬───┬───┐')
#     middle_1 = '  1  ' + (('│' + f' {x} ') * 3 + '│')
#     bottom_1 = (' ' * 5 + '├───┼───┼───┤')
#
#     middle_2 = '  2  ' + (('│' + f' {x} ') * 3 + '│')
#     bottom_2 = bottom_1
#
#     middle_3 = '  3  ' + (('│' + f' {x} ') * 3 + '│')
#     bottom_3 = (' ' * 5 + '└───┴───┴───┘')
# ---------------------------------------------------
# def show_fields(f, free_cell):
#     print('\u2193x\y\u2192', end=' ' * 2)
#     print('1' + ' ' * 3 + '2' + ' ' * 3 + '3')
#
#     if f[0] == 'X':
#         x = f'\033[1m\033[34m{f[0]}\033[0m'
#     elif f[0] == 'O':
#         x = f'\033[1m\033[36m{f[0]}\033[0m'
#         x = '\u2087'
#         x = 7
#         x = f'\033[2m\033[3m\033[37m{x}\033[0m'
#
#     top_1 = (' ' * 5 + '\u250c' + '\u2500' * 3 + '\u252c' + '\u2500' * 3 + '\u252c' + '\u2500' * 3 + '\u2510')
#     middle_1 = '  1  ' + (('\u2502' + f' {x} ') * 3 + '\u2502')
#     bottom_1 = (' ' * 5 + '\u251c' + '\u2500' * 3 + '\u253c' + '\u2500' * 3 + '\u253c' + '\u2500' * 3 + '\u2524')
#
#     middle_2 = '  2  ' + (('\u2502' + f' {x} ') * 3 + '\u2502')
#     bottom_2 = bottom_1
#
#     middle_3 = '  3  ' + (('\u2502' + f' {x} ') * 3 + '\u2502')
#     bottom_3 = (' ' * 5 + '\u2514' + ('\u2500' * 3 + '\u2534') * 2 + '\u2500' * 3 + '\u2518')
#
#     lst = [top_1, middle_1, bottom_1, middle_2, bottom_2, middle_3, bottom_3]
#     for i in lst:
#         if i == middle_1:
#             x = 'W'
#         elif i == middle_2:
#             x = 'Z'
#         print(i)
#     # return True
# -------------------------------------------------
# def show_field(f):
#     # num ='  0 1 2'
#     # print(num)
#     # #zip
#     # for row,i in zip(f,num.split()):
#     #     print (f"{i} {' '.join(str(j) for j in row)}")
#
#     x = '_'
#
#     s_top = '  ' + ('\u250c' + '\u2500' * 3 + '\u2510' + ' ') * 3
#     s_middle = '0 ' + ('\u2502' + f' {x} ' + '\u2502' + ' ') * 3
#     s_bottom = '  ' + ('\u2514' + '\u2500' * 3 + '\u2518' + ' ') * 3
#
#     l = [s_top, s_middle, s_bottom] * 3
#
#     # print("\u2193x\y\u2192 " + '\n')
#     # print('\u2193x\y\u2192 ' + '\n')
#     # print('\u2193x\y-\u27A1 ' +'\n')
#     print("\u2193x\y\u2192", end=' ')
#     print('    0     1     2')
#     for i in l:
#         print(i)
# -------------------------------------------
# x = 7
# x = '\u2077'
# # x = '\u2087'
# x = f'\033[2m\033[3m\033[37m{x}\033[0m'

# x = 'X'
# x = f'\033[1m\033[34m{x}\033[0m'

# print('\u2193x\y-\u27A1 ' +'\n')
# --------------------------------------
# s_top_2 = ('\u250c'+'\u2500'*3+'\u252c'+'\u2500'*3+'\u252c'+'\u2500'*3+'\u2510')
# s_bottom_3 = ('\u2514'+'\u2500'*3+'\u2518'+'\u2500'*3 +'\u253c'+'\u2500'*3+'\u2524')
    # print('\u2193x\y\u2192', end=' '*2)
# --------------------------------------
# elif place[0] == 'q':
#     print('Вы вышли из игры')
#     fr_cell = [1]
#     cell = 1
#     break
# field[x][y] = user

# --------------------------------------
# if not (x >= 0 and x < 3 and y >= 0 and y < 3):
# place = list(map(int, place))
# step = 0  # Номер хода
# if f[x][y]!='-':
#     print('Клетка занята')
#     continue
# --------------------------------------
# if win_position(field, user):
# --------------------------------------
# start(field)
# "field - содержит кортеж из user (X или O) и номер клетки от 1 до 9"
# -------------------------------------
# def foo(a, b: 'annotating b', c: int) -> float:
#     print(a + b + c)
# def win_position(field: str, user: str):
# -------------------------------------
# field = [['_'] * 3 for _ in range(3)]

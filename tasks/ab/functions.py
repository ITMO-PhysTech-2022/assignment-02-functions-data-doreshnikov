from typing import Any, Callable


# BASE

def useless_function():
    """
    Эта функция должна ничего не делать и ничего не возвращать
    Зачем она здесь?... Никто не знает :(
    """
    # SOLUTION
    return  # моментальный выход из функции

    print('What is happening?...')
    print('Why is it happening?...')
    if True is False:
        exit(1)  # beautiful death
    return UserWarning


def print_tree(size: int):
    """
    Функция выводит елочку из size сегментов размерами от 1 до size
    """

    def _print_segment(height: int):
        """
        Функция выводит сегмент елочки размера height
        """
        # сегмент имеет height строк, каждая ширины 2 * size - 1
        for line in range(height):
            # строка номер line содержит 2 * line + 1 звезд
            stars = '*' * (2 * line + 1)
            # форматная строка - дополнить
            #  > пробелами (' ')
            #  > поровну слева и справа ('^')
            #  > до длины 2 * size - 1
            print(f'{stars: ^{2 * size - 1}}')
            # альтернативно: side = (2 * size - 1 - stars) // 2; print(' ' * side + stars)

    # печатаем по очереди все сегменты
    for i in range(size):
        _print_segment(i + 1)


# RECURSION

def generate_json(depth: int):
    """
    Функция генерирует словарь (dict) с уровнем вложенности depth
    """
    result = {'a': 'value 1', 'b': 'value 2'}
    if depth == 1:
        # если на последнем слое, то просто создаем третье значение
        result['c'] = 'value 3'
    else:
        # иначе генерируем под-словарь уровнем на 1 меньше
        result['c'] = generate_json(depth - 1)
    return result


'''
Пояснения:

1. _worker(0) заново вызывает wtf()
это бесконечная рекурсия, нам не подходит
2. _worker(нечетного) 
- поделит аргумент на 3 
- и вернет результат на 1 больше полученного
3. _worker(делящегося на 982) 
- сохранит делимость на 982
- поэтому рекурсивный вызов пойдет в ту же ветку
- пока аргумент не достигнет 10000, после чего будет вызван _worker(x - 2)
- x - 2 четный и не делится на 982, поэтому следующий вызов уйдет в последнюю ветку и вернет 0

Итого:
- нам не подходит _worker(0)
- не подходит _worker(982k), накопится слишком маленький ответ (около 10000 / 982)
- не подходит _worker(3**k), так как придет в 9 -> 3 -> 1 -> 0, уйдет в бесконечную рекурсию
=>
- надо комбинировать переходы по второму и третьему условию
    > x -> x // 3 -> ... -> x // (3 ** k) ->
    > -> x // (3 ** k) + 982 -> ...
- при чем все деления на 3, кроме последнего, должны оставлять число нечетным

Рассмотрим 982 * 3 + 1, оно нечетно, и при вызове от него сначала случится деление на 3,
а затем все уйдет в 11 шагов по третьей ветке условий
Чтобы получить ответ 42, надо набрать еще 30 шагов делений на 3, то есть
!!! x = (982 * 3 + 1) * (3 ** 30) = 606761166282930603
'''


def wtf():
    """
    Функция wtf вызывает внутреннюю функцию _worker с некоторым аргументом
    и должна возвращать число 42
    """

    def _worker(x):
        if x == 0:
            return wtf()
        elif x % 2 == 1:
            return _worker(x // 3) + 1
        elif x % 982 == 0:
            return _worker(x + 982 if x < 10000 else x - 2) + 1
        else:
            return 0

    return _worker(606761166282930603)


# ARGS, KWARGS

def mex(*args):
    """
    Функция принимает произвольное число аргументов и возвращает их mex,
    то есть minimal excluded - минимальное целое неотрицательное число,
    отсутствующее среди них
    """
    # рассмотрим все уникальные аргументы в порядке возрастания
    items = sorted(set(args))
    for i in range(len(items)):
        # если на i-м месте стоит не i, то i - первое отсутствующее число
        # например, 0 1 2 3 5 - на позициях 0, 1, 2, 3 все ок, на позиции 4 нет числа 4
        if items[i] != i:
            return i
    # если такое не нашлось, то первое отсутствующее равно len(items)
    # например, 0 1 2 3 4 - отсутствует число 5
    return len(items)


def replace_keys(data: dict[str, Any], **kwargs: str):
    """
    Функция принимает словарь со строковыми ключами и набор аргументов вида
    key=value, и возвращает копию этого словаря, в котором каждый ключ key
    переименован в соответствующий ему value
    """
    result = {}
    for key, value in data.items():
        if key in kwargs:
            # если есть переименование, переименуем
            result[kwargs[key]] = value
        else:
            # иначе оставим как есть
            result[key] = value

    # альтернативно - в одну строку
    # (полезный метод .get с возможностью указать значение по умолчанию)
    result = {kwargs.get(key, key): data[key] for key in data}
    return result


# HIGH ORDER

def count_calls_until(f: Callable, start, condition: Callable[..., bool]):
    """
    Функция принимает другую функцию от одного аргумента f, начальное значение
    и условие остановки, и возвращает количество последовательных вызовов f от
    значения start, пока результат не начнет удовлетворять условию остановки
    """
    counter = 0
    value = start
    while not condition(value):
        # пока не выполнится условие, будем применять f и увеличивать счетчик
        value = f(value)
        counter += 1
    return counter


def bind(f: Callable, **kwargs):
    """
    Функция принимает другую функцию от произвольного набора аргументов f и
    возвращает новую функцию, вызов которой идентичен вызову f, но с уже
    заранее подставленными указанными в **kwargs аргументами
    """

    def new_f(*args):
        # сколько всего аргументов будет передано в f
        n = len(args) + len(kwargs)
        new_args = [None for _ in range(n)]
        next_arg = 0  # номер следующего неиспользованного аргумента из args

        for i in range(n):
            if f'_{i + 1}' in kwargs:
                # если аргумент был предподставлен, возьмем предподставленное значение
                new_args[i] = kwargs[f'_{i + 1}']
            else:
                # иначе используем следующий переданный не-предподставленный аргумент
                new_args[i] = args[next_arg]
                next_arg += 1

        return f(*new_args)

    return new_f


if __name__ == '__main__':
    print('-' * 30)
    print(useless_function())

    print('-' * 30)
    print_tree(3)
    print_tree(5)

    print('-' * 30)
    print(generate_json(1))
    print(generate_json(3))

    print('-' * 30)
    print(wtf())

    print('-' * 30)
    print(mex(1, 5, 3, 0, 2, 6))
    print(mex(1, 2, 3, 4))

    print('-' * 30)
    print(replace_keys({'x': 1, 'y': 2}, x='z'))
    print(replace_keys({'x': 1, 'y': 2, 'z': 3}, x='y', y='z', z='x', p='q'))

    print('-' * 30)
    print(count_calls_until(
        lambda x: x + 2,
        0,
        lambda x: x > 10
    ))
    print(count_calls_until(
        lambda x: x // 10,
        1257513,
        lambda x: x == 0
    ))

    print('-' * 30)


    def f(x, y):
        return x - y


    fx = bind(f, _1=10)  # эквивалентно функции fx(y): return 10 - y
    print(fx(1), fx(10), fx(15))  # 9, 0, -5

    fy = bind(f, _2=10)  # эквивалентно функции fy(x): return x - 10
    print(fy(7), fy(11), fy(13))  # -3, 1, 3

    fxy = bind(f, _1=22, _2=31)  # эквивалентно функции fxy(): return 22 - 31
    print(fxy())  # -9

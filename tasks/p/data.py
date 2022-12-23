from typing import Any


# STRINGS

def censor(s: str, blacklist: list[str]):
    """
    Функция принимает строку и список запрещенных подстрок, и возвращает копию
    строки s, в которой все вхождения запрещенных слов заменены на равное их
    длине количество '*'
    """
    for word in blacklist:
        replacement = '*' * len(word)  # замена для слова
        s = s.replace(word, replacement)
    return s


def shorten(s: str, size: int):
    """
    Функция принимает строку s и возвращает ее укороченную до длины size версию,
    в которой от s оставлены lower-case начало и конец с '...' между ними, а
    все блоки пробельных символов заранее заменены на '-'
    """
    s = s.lower().replace(' ', '-')
    if len(s) <= size:
        return s
    side = (size - 2) // 2  # длина префикса и суффикса
    dots = '..' if size % 2 == 0 else '...'
    return s[:side] + dots + s[-side:]


# LISTS

def windowed_average(array: list, k: int):
    """
    Функция принимает массив array и ширину "окна" k, и возвращает массив,
    состоящий из средних арифметических значений массива array на каждом его
    подотрезке длины k
    """
    result = []
    for start in range(len(array) - k + 1):
        # можно написать более быстрое решение, но это более компактное
        average = sum(array[start: start + k]) / k  # среднее на отрезке [start, start + k)
        result.append(average)
    return result


def shuffle(array: list, times: int = 1):
    """
    Функция принимает массив array и количество "перетасовок", и возвращает
    копию этого массива, перетасованную times раз делением пополам и
    смешиванием двух полученных половин
    """
    n = len(array)

    for i in range(times):
        # сделать одно перемешивание
        # 1. разбить на две половины
        sep = n // 2
        left, right = array[:sep], array[sep:]
        # 2. поочередно набрать элементы
        array = []
        for j in range(n):
            if j % 2 == 0:
                array.append(right[j // 2])
            else:
                array.append(left[j // 2])
        # 3. записать в массив через один
        array[::2] = right
        array[1::2] = left

    return array


# SETS

def is_unrestricted(item):
    """
    Функция принимает произвольный объект и возвращает, может ли он быть
    элементом множества
    """
    s = set()
    try:
        # попробуем добавить элемент в множество
        s.add(item)
        return True
    except TypeError:
        # если случилась ошибка, вернем, что нельзя
        return False


def update_squares(s: set[int]):
    """
    Функция принимает множество целых чисел и добавляет в него квадрат каждого
    из его изначальных элементов
    (функция модифицирует переданный объект и ничего не возвращает)
    """
    new_elements = set()
    for item in s:
        new_elements.add(item ** 2)
    s.update(new_elements)


# DICTIONARIES

def select(d: dict, *args):
    """
    Функция принимает словарь d и набор ключей, и возвращает копию d, в которой
    оставлены только ключи из *args, при чем если какой-то ключ из *args в d
    отсутствовал, в возвращаемом словаре по этому ключу должен лежать None
    """
    result = {}
    for key in args:
        result[key] = d.get(key)
    return result
    # альтернативное решение (более короткое)
    return {key: d.get(key) for key in args}


if __name__ == '__main__':
    print('-' * 30)
    print(censor('Hello world!', ['world']))
    print(censor('I am inevitable', ['I', 'inevi']))

    print('-' * 30)
    print(shorten('World', 4))
    print(shorten('Task number 1 Data', 15))

    print('-' * 30)
    print(windowed_average([1, 3, 5, 7, 9], 2))
    print(windowed_average([1, 5, 7, 10, 18], 4))

    print('-' * 30)
    print(shuffle([1, 2, 3, 4, 5], 1))
    print(shuffle([1, 2, 3, 4], 3))

    print('-' * 30)
    print(is_unrestricted([]))
    print(is_unrestricted((1, 2, (3, 4))))
    print(is_unrestricted(357235))
    print(is_unrestricted("112"))
    print(is_unrestricted((1, 2, {3, 4})))

    print('-' * 30)
    s = {1, 2, 3}
    update_squares(s)
    print(s)
    s = {-1, 1}
    update_squares(s)
    print(s)
    s = {2, 4, 16}
    update_squares(s)
    print(s)

    print('-' * 30)
    print(select({'name': 'Barsik', 'age': 10, 'job': 'Cat'}, 'name', 'age'))
    print(select({'name': 'Barsik', 'job': 'Cat'}, 'name', 'age'))
    print(select({}, 'x', 'y', 'z'))
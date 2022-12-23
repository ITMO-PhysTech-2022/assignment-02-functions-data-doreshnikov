from typing import Callable


# RECURSION

def rprint(array: list, max_depth: int = -1):
    """
    Функция принимает массив со вложенными массивами и выводит его с точностью
    до глубины max_depth, заменяя все более глубокие элементы на '...'
    """

    def _worker(obj, depth: int):
        """
        Возвращает строку-представление объекта obj
        если этот объект находится на глубине depth
        в исходном массиве
        """
        if not isinstance(obj, list):
            return str(obj)
        if depth == max_depth:
            return '[...]'
        results = []
        for item in obj:
            result = _worker(item, depth + 1)
            results.append(result)
        return '[' + ', '.join(results) + ']'

    print(_worker(array, 0))


# ARGS, KWARGS

def median(*args, low: bool = True):
    """
    Функция принимает произвольное число аргументов и возвращает медиану
    (если low = True, то при четном числе элементов возвращается меньшая из
    двух медиан, иначе - большая)
    """
    sorted_args = sorted(args)
    pos = len(args) // 2
    if low and len(args) % 2 == 0:
        pos -= 1
    return sorted_args[pos]


def sequential_replace(s: str, **kwargs: str):
    """
    Функция принимает строку s и набор аргументов вида key=value и возвращает
    строку s, в которой все вхождения подстрок key заменены на подстроки value
    (гарантируется, что все вхождения ключей в s не пересекаются)
    """
    for k, v in kwargs.items():
        # заменяем вхождения k на v
        s = s.replace(k, v)
    return s


def signature(
        a, b=0, c=0, /,
        start=0, *,
        mode, inplace=False
):
    """
    Функция должна иметь возможность быть вызванной только указанным в условии
    образом (при этом не должна что-либо делать)
    """
    pass


# HIGH ORDER

def twice(f: Callable):
    """
    Функция принимает другую функцию от одного аргумента f и возвращает новую
    функцию от одного аргумента, выполняющую двойное применение f
    (например, при f(x) -> x + 5 и g = twice(f), верно g(x) -> x + 10)
    """

    def new_function(x):
        res1 = f(x)
        res2 = f(res1)
        return res2

    return new_function


def logging(f: Callable):
    """
    Функция принимает другую функцию от произвольного набора аргументов f и
    возвращает новую функцию, которая копирует поведение f, но перед каждым
    вызовом выводит все переданные в нее аргументы
    """

    def _invoke(*args, **kwargs):
        print(args, kwargs)
        return f(*args, **kwargs)

    return _invoke


if __name__ == '__main__':
    print('-' * 30)
    rprint([1, [2], [[3]], [[[4]]]], 2)
    rprint([1, [2, 3], [[4, [5], [6, [7], [[[8]]]]]], [9]], 3)
    rprint([1, 2, 3], 0)

    print('-' * 30)
    print(median(4, 3, 5, 1, 2))
    print(median(6, 2, 1, 4, 5, 3))
    print(median(6, 2, 1, 4, 5, 3, low=False))

    print('-' * 30)
    print(sequential_replace('i am a cat', i='you', am='are', cat='human'))
    print(sequential_replace('defeat is not an option', defeat='option', option='defeat', an='a'))
    print(sequential_replace('subwords can also be replaced', sub='', laced='eated'))

    signature(1, mode='print')
    signature(1, 2, 3, mode='precalc', inplace=True)
    signature(1, 2, 3, start=0, mode='print', inplace=False)
    signature(1, 2, 3, 0, mode='print')


    # signature(1)
    # signature(mode='print')
    # signature(a=1, b=2, start=3, mode='precalc')
    # signature(1, 2, 3, 0, 'print')

    def f1(x):
        return x + 2


    def f2(x):
        return x ** 2


    def f3(x):
        print(x)
        return x


    print('-' * 30)
    print(twice(f1)(2))
    print(twice(f2)(3))
    print(twice(f3)(4))

    print('-' * 30)


    def f(x, y, z, opt=False):
        if opt:
            return max(x, y, z)
        return min(x, y, z)


    g = logging(f)
    x = g(1, 2, 3, opt=True)
    y = g(6, 5, 4)
    print(x, y)

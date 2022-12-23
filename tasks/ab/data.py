# STRINGS

def wordcount(s: str):
    """
    Функция принимает строку s и возвращает словарь, считающий количество
    вхождений каждого слова в нее
    (слова стоит рассматривать без учета регистра и без знаков препинания)
    """
    words = s.split()

    # BASIC
    count = {}
    for word in words:
        # то же, что и `count[word] + 1 if word in count else 1`
        count[word] = count.get(word, 0) + 1

    # ADVANCED
    count = {}
    for word in words:
        word = word.lower()  # перевели в нижний регистр
        new_word = ''
        for symbol in word:
            # оставили только алфавитные символы
            if symbol.isalpha(): new_word += symbol
        count[new_word] = count.get(new_word, 0) + 1

    return count


def caesar_encode(s: str, shift: int):
    """
    Функция принимает строку s и величину сдвига shift и возвращает результат
    применения шифра Цезаря к строке, со сдвигом на shift влево
    """
    # ADVANCED
    result = ''

    for symbol in s:
        # не-буквенные символы оставляем как есть
        if not symbol.isalpha():
            result += symbol
            continue
        # относительная позиция буквы в алфавите
        i = ord(symbol.lower()) - ord('a')
        # буква на shift позиций по циклу левее
        new_c = chr(ord('a') + (i - shift) % 26)
        # та же буква, но в исходном регистре
        result += new_c if symbol.islower() else new_c.upper()

    return result


# Упражнение на функции:
# определите дешифратор для шифра Цезаря, используя только вызов шифратора
caesar_decode = lambda s, shift: caesar_encode(s, -shift)


# LISTS

def extract_each(array: list, k: int, cyclic: bool = False):
    """
    Функция принимает массив array и число k, и возвращает массив, состоящий из
    каждого k-го элемента массива array
    (если передан cyclic=True, при достижении конца массива выбор элементов
    продолжается с начала, пока не достигнет уже выбранного элемента)
    """
    # BASIC
    result = array[::k]  # да, это все..

    # ADVANCED
    if len(array) == 0: return []  # отдельная проверка случая пустого массива
    result = []
    used = set()  # множество уже взятых позиций
    current = 0  # текущая позиция
    while current not in used:
        # добавляем текущий элемент и запоминаем позицию
        result.append(array[current])
        used.add(current)
        # переходим к следующему
        current += k
        if current >= len(array):
            if not cyclic:
                break
            else:
                current = current % len(array)

    return result


# SETS

def compare(s1: set[int], s2: set[int]):
    """
    Функция принимает два множества чисел и возвращает результат их сравнения -
    меньшим считается то множество, в котором лежит наименьший из их не-общих
    элементов
    """
    # находим минимум в s1 - s2 (или -inf, если разность пустая)
    min_left = min(s1 - s2, default=float('-inf'))
    # находим минимум в s2 - s1 (или -inf, если разность пустая)
    min_right = min(s2 - s1, default=float('-inf'))
    return min_left < min_right


# DICTIONARIES

def merge(d1: dict, d2: dict, recursive: bool = False):
    """
    Функция принимает два json-словаря и возвращает результат их объединения
    (при наличии одинаковых ключей recursive=False означает, что надо оставить
    значение из d1, а recursive=True - что значения надо объединить рекурсивно)
    """
    # просто для копирования объектов
    from copy import deepcopy

    # BASIC
    # return d1 | d2  # начиная с питона 3.9 - объединение словарей

    # BASIC v2
    result = deepcopy(d2)
    for k, v in d1.items():
        # для каждого ключа в d1 выставляем соответствующее значение
        result[k] = v

    # ADVANCED
    result = deepcopy(d2)
    for k, v in d1.items():
        if recursive and k in result and \
                isinstance(result[k], dict) and isinstance(v, dict):
            # если ключ был и оба значения - словари, вызываем merge
            # важен порядок: сначала v (из d1), потом result[k] (из d2)
            # и надо передать дальше флаг recursive
            result[k] = merge(v, result[k], recursive)
        else:
            # иначе просто выставляем значение
            result[k] = v

    return result


def translate_back(d: dict[str, list[str]]):
    """
    Функция принимает словарь, задающий возможные способы перевода слов с
    одного языка на другой, и возвращает словарь, описывающий перевод в
    обратном направлении
    """
    result = {}
    for word, translations in d.items():
        # для каждой пары (слово -> переводы)
        for translation in translations:
            if translation not in result:
                # если translation не было в новом словаре, то добавляем пустой список переводов
                result[translation] = []
            # добавляем word в качестве возможного перевода
            result[translation].append(word)
    return result


if __name__ == '__main__':
    print('-' * 30)
    print(wordcount('hello world hello'))
    print(wordcount(''))
    print(wordcount('i am who i am'))

    print('-' * 30)
    print(caesar_encode('caesar', 1))
    print(caesar_encode('Encode this', 11))
    print(caesar_decode('bzdrzq', 1))
    print(caesar_decode('Tcrdst iwxh', 11))

    print('-' * 30)
    print(extract_each([1, 2, 3, 4], 1))
    print(extract_each([1, 2, 3, 4], 3))
    print(extract_each([1, 2, 3, 4], 3, True))

    print('-' * 30)
    print(compare({1, 2, 3}, {1, 2, 3}))
    print(compare({1, 2}, {1, 2, 3}))
    print(compare({1, 2, 4}, {1, 2, 5}))

    print('-' * 30)
    print(merge({'x': 10}, {'y': 20}))
    print(merge({'x': 10}, {'x': 20}))
    print(merge({'x': {'y': 20}}, {'x': {'z': 30}}))
    print(merge({'x': {'y': 20}}, {'x': {'z': 30}}, True))

    print('-' * 30)
    print(translate_back({
        'apple': ['malum', 'pomum', 'popula'],
        'fruit': ['popum'],
        'punishment': ['malum', 'multa']
    }))

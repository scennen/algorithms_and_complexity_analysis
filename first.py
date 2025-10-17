import time
import tracemalloc
import functools
import threading
import psutil
import os


def timeit(func):
    """
    Декоратор для измерения времени работы функции.
    Суммирует время всех рекурсивных вызовов (если функция сама себя вызывает).
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not hasattr(wrapper, "_time_acc"):
            wrapper._time_acc = 0.0
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            end = time.perf_counter()
            wrapper._time_acc += (end - start)
            # если это внешний вызов (не рекурсивный), то печатаем и сбрасываем
            # мы определим «внешний вызов» как момент, когда стек глубже, чем вызов функции
            wrapper._recursion_depth -= 1
            if wrapper._recursion_depth == 0:
                total = wrapper._time_acc
                # сброс для следующего полного запуска
                wrapper._time_acc = 0.0
                print(f"[timeit] Function {func.__name__} took total {total:.6f} seconds")
        # Для корректного определения рекурсии:

    def new_wrapper(*args, **kwargs):
        if not hasattr(wrapper, "_recursion_depth"):
            wrapper._recursion_depth = 0
        wrapper._recursion_depth += 1
        return wrapper(*args, **kwargs)

    return new_wrapper


def memoryit(func):
    """
    Декоратор для измерения пикового использования памяти Python во время работы функции.
    Использует tracemalloc для Python-памяти + psutil для общего RSS процесса.
    Аккумулирует пиковые значения в рекурсии.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # инициализация
        if not hasattr(wrapper, "_mem_peak_python"):
            wrapper._mem_peak_python = 0
            wrapper._mem_peak_rss = 0
        if not hasattr(wrapper, "_call_depth"):
            wrapper._call_depth = 0

        if wrapper._call_depth == 0:
            # первый (внешний) вызов — запускаем трассировку
            tracemalloc.start()
        wrapper._call_depth += 1

        rss_before = psutil.Process(os.getpid()).memory_info().rss

        try:
            return func(*args, **kwargs)
        finally:
            current, peak = tracemalloc.get_traced_memory()
            rss_after = psutil.Process(os.getpid()).memory_info().rss

            # обновляем пик Python-аллокатора
            if peak > wrapper._mem_peak_python:
                wrapper._mem_peak_python = peak
            # обновляем пик RSS
            rss_delta = rss_after - rss_before
            if rss_delta > wrapper._mem_peak_rss:
                wrapper._mem_peak_rss = rss_delta

            wrapper._call_depth -= 1
            if wrapper._call_depth == 0:
                # завершение внешнего вызова
                tracemalloc.stop()
                # вывод результатов
                print(
                    f"[memoryit] Function {func.__name__} peak python allocation: {wrapper._mem_peak_python / 1024:.2f} KiB")
                print(f"[memoryit] Function {func.__name__} peak RSS delta: {wrapper._mem_peak_rss / 1024:.2f} KiB")
                # сброс для следующего вызова
                wrapper._mem_peak_python = 0
                wrapper._mem_peak_rss = 0

    return wrapper


@timeit
@memoryit
def symmetric_difference(input_str: str) -> str:
    set_a = []  # Множество A
    set_b = []  # Множество B
    result = []
    input_list = input_str.split(' ')

    is_b = False

    for symbol in input_list:  # Для заполнения 2 множеств
        if int(symbol) == 0:
            is_b = True
            continue
        elif is_b == False:
            set_a.append(symbol)
        else:
            set_b.append(symbol)

    for i in set_a:
        if i not in set_b:
            result.append(i)

    for j in set_b:
        if j not in set_a:
            result.append(j)

    result.sort()

    if len(result) == 0:
        return "0"
    else:
        return ' '.join(map(str, result))


# print(symmetric_difference('1500 7800 12345 567 8900 4321 9999 150 6789 3210 2555 7777 11111 5432 8888 6666 4444 2222 3333 5555 0 7800 567 8900 20000 150 123 4567 9999 4321 6789 3210 11111 8888 6666 4444 0'))
# print(symmetric_difference('100 200 300 400 500 600 700 800 900 1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000 2100 2200 2300 2400 2500 0 50 150 250 350 450 550 650 750 850 950 1050 1150 1250 1350 1450 1550 1650 1750 1850 1950 2050 2150 2250 2350 2450 0'))
# print(symmetric_difference('42 1984 2023 777 1337 69 420 1234 5678 9999 11111 15555 17777 19999 2468 13579 8642 7531 2222 3333 4444 5555 6666 7777 8888 0 42 777 1337 10000 15000 20000 2468 8642 2222 4444 6666 8888 11111 15555 17777 19999 0'))
# print(symmetric_difference('1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 0 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 0'))
# print(symmetric_difference('15000 2500 7500 12500 500 17500 1000 20000 3000 4000 6000 7000 8000 9000 11000 12000 13000 14000 16000 17000 18000 19000 0 2500 7500 12500 17500 333 666 999 1333 1666 1999 2333 2666 2999 3333 3666 3999 4333 4666 4999 0'))
# print(symmetric_difference('111 222 333 444 555 666 777 888 999 1111 2222 3333 4444 5555 6666 7777 8888 9999 11111 12222 13333 14444 15555 16666 17777 18888 19999 0 222 444 666 888 1111 3333 5555 7777 9999 12222 14444 16666 18888 20000 12345 13579 14789 15987 0'))
# print(symmetric_difference('123 456 789 1011 1213 1415 1617 1819 2021 2223 2425 2627 2829 3031 3233 3435 3637 3839 4041 4243 4445 4647 4849 5051 5253 5455 5657 5859 6061 6263 0 456 789 1011 1415 1819 2223 2627 3031 3435 3839 4243 4647 5051 5455 5859 6263 6666 7777 8888 9999 11111 0'))
# print(symmetric_difference('5000 10000 15000 2000 4000 6000 8000 12000 14000 16000 18000 2500 3500 4500 5500 6500 7500 8500 9500 10500 11500 12500 13500 14500 15500 16500 17500 18500 19500 0 2000 4000 6000 8000 10000 12000 14000 16000 18000 2500 4500 6500 8500 10500 12500 14500 16500 18500 19500 333 666 999 0'))
# print(symmetric_difference('11111 12222 13333 14444 15555 16666 17777 18888 19999 20000 1111 2222 3333 4444 5555 6666 7777 8888 9999 1234 2345 3456 4567 5678 6789 7890 8901 9012 1357 2468 3579 4680 5791 6802 7913 8024 9135 0 12222 14444 16666 18888 20000 2222 4444 6666 8888 2345 4567 6789 8901 2468 4680 6802 8024 10000 15000 0'))
# print(symmetric_difference('19999 20000 1 2 3 4 5 6 7 8 9 10 100 200 300 400 500 600 700 800 900 1000 1111 2222 3333 4444 5555 6666 7777 8888 9999 12345 13579 14999 15999 16999 17999 18999 0 1 3 5 7 9 100 300 500 700 900 1111 3333 5555 7777 9999 12345 14999 15999 17999 18999 20000 42 142 242 342 442 0'))


@timeit
@memoryit
def long_a_s(first_operand: str, operator: str, second_operator: str) -> str:
    if operator == "+":
        return int(first_operand) + int(second_operator)
    elif operator == "-":
        return int(first_operand) - int(second_operator)
    else:
        pass  # Место для новых операторов


print(long_a_s('1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890', '+', '9876543210987654321098765432109876543210987654321098765432109876543210987654321098765432109876543210'))
print(long_a_s('9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999', '-', '1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'))
print(long_a_s('5000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', '+', '5000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'))
print(long_a_s('1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', '-', '1'))
print(long_a_s('2468135790246813579024681357902468135790246813579024681357902468135790246813579024681357902468135790', '+', '7531986420753198642075319864207531986420753198642075319864207531986420753198642075319864207531986420'))


@timeit
@memoryit
def maharajah(size: int, amount: int) -> int:
    pass

@timeit
@memoryit
def () -> :
    pass


@timeit
@memoryit
def () -> :
    pass


@timeit
@memoryit
def () -> :
    pass


@timeit
@memoryit
def () -> :
    pass


@timeit
@memoryit
def () -> :
    pass


@timeit
@memoryit
def () -> :
    pass


@timeit
@memoryit
def () -> :
    pass
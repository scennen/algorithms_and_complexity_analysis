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
    zero_index = input_str.find('0')  # Разделитель
    set_a = input_str[:zero_index - 1]  # Множество A
    set_b = input_str[zero_index+2:len(input_str)-2]  # Множество B
    print(set_a)
    print(set_b)
    # for num in set_a:
    #     if num in set_b:

    result_output = []


symmetric_difference('1 2 6 8 7 3 0 4 1 6 2 3 9 0')

# если 1 в set_b? да -> удаляем, иначе в result_output
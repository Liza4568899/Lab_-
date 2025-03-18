import time
import multiprocessing
import random
from decimal import Decimal, getcontext
from concurrent.futures import ThreadPoolExecutor


def harmonic_sum_sequential(n, precision):
    getcontext().prec = precision + 5
    total = Decimal(0)
    for i in range(1, n + 1):
        total += Decimal(1) / Decimal(i)
    return round(total, precision)


def harmonic_partial(start, end, precision):
    getcontext().prec = precision + 5
    partial_sum = Decimal(0)
    for i in range(start, end + 1):
        partial_sum += Decimal(1) / Decimal(i)
    return partial_sum


def harmonic_sum_parallel(n, precision):
    getcontext().prec = precision + 5
    num_processes = min(multiprocessing.cpu_count(), n // 1000) if n > 10000 else 1
    num_processes = max(1, num_processes)

    with multiprocessing.Pool(num_processes) as pool:
        step = n // num_processes
        ranges = [(i * step + 1, (i + 1) * step if i < num_processes - 1 else n, precision) for i in
                  range(num_processes)]
        partial_sums = pool.starmap(harmonic_partial, ranges)

    return round(sum(partial_sums), precision), num_processes


def harmonic_sum_threads(n, precision):
    getcontext().prec = precision + 5
    max_threads = min(n // 500, multiprocessing.cpu_count()) if n > 10000 else 1
    num_threads = max(1, max_threads)

    step = n // num_threads
    ranges = [(i * step + 1, (i + 1) * step if i < num_threads - 1 else n, precision) for i in range(num_threads)]

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        partial_sums = list(executor.map(lambda args: harmonic_partial(*args), ranges))

    return round(sum(partial_sums), precision), num_threads


def read_input_from_file(filename):
    try:
        with open(filename, "r") as f:
            data = f.readlines()
            n = int(data[0].strip().split("=")[1])
            precision = int(data[1].strip().split("=")[1])
            return n, precision
    except Exception as e:
        print(f"Помилка читання файлу: {e}")
        return None, None


def generate_random_input():
    n = random.randint(100, 10000)
    precision = random.randint(2, 10)
    print(f"Згенеровано випадкові значення: n={n}, precision={precision}")
    return n, precision


def main():
    choice = input("Виберіть спосіб введення даних (1 - вручну, 2 - з файлу input.txt, 3 - випадково): ")

    if choice == "2":
        n, precision = read_input_from_file("input.txt")
        if n is None or precision is None:
            return
    elif choice == "3":
        n, precision = generate_random_input()
    else:
        n = int(input("Введіть кількість членів ряду: "))
        precision = int(input("Введіть кількість знаків після коми: "))
        with open("input.txt", "w") as f:
            f.write(f"n={n}\nprecision={precision}\n")

    start_seq = time.perf_counter()
    result_seq = harmonic_sum_sequential(n, precision)
    time_seq = time.perf_counter() - start_seq

    start_par = time.perf_counter()
    result_par, num_processes = harmonic_sum_parallel(n, precision)
    time_par = time.perf_counter() - start_par

    start_thr = time.perf_counter()
    result_thr, num_threads = harmonic_sum_threads(n, precision)
    time_thr = time.perf_counter() - start_thr

    with open("output.txt", "w") as f:
        f.write(f"Послідовний результат: {result_seq} (час: {time_seq:.5f} сек)\n")
        f.write(
            f"Паралельний результат (multiprocessing): {result_par} (час: {time_par:.5f} сек, процеси: {num_processes})\n")
        f.write(
            f"Паралельний результат (multithreading): {result_thr} (час: {time_thr:.5f} сек, потоки: {num_threads})\n")

    print("Результати збережені у output.txt")
    print(f"Послідовний результат: {result_seq} (час: {time_seq:.5f} сек)")
    print(f"Паралельний результат (multiprocessing): {result_par} (час: {time_par:.5f} сек, процеси: {num_processes})")
    print(f"Паралельний результат (multithreading): {result_thr} (час: {time_thr:.5f} сек, потоки: {num_threads})")


if __name__ == "__main__":
    main()

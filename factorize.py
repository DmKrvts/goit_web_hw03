from multiprocessing import Pool, cpu_count
import logging
import time


logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')


def factorize_synk(*numbers):
    result = []
    for item in numbers:
        temp_list = []
        for i in range(1, item + 1):
            if item % i == 0:
                temp_list.append(i)
        result.append(temp_list)
    return result


def test_factorize():
    start_time = time.time()
    a, b, c, d = factorize_synk(128, 255, 99999, 10651060)
    end_time = time.time()
    logging.debug(f"Res-time sync {end_time - start_time}")

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
                 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]


def factorize_single(num):
    factors = []
    for i in range(1, num + 1):
        if num % i == 0:
            factors.append(i)
            print(i)
    print(f"parallel res {factors}")
    return factors

def factorize_parallel(*numbers):    
    with Pool(cpu_count()) as p:
        result = p.map(factorize_single, numbers)
    return result


def test_factorize_parallel():
    start_time = time.time()
    a, b, c, d = factorize_parallel(128, 255, 99999, 10651060)
    end_time = time.time()
    logging.debug(f"Res-time parallel {end_time - start_time}")

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
                 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]


if __name__ == "__main__":
    test_factorize()
    test_factorize_parallel()
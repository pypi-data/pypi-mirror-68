import random
import time
from multiprocessing import Pool, cpu_count


def f(x):
    return x * x


if __name__ == '__main__':
    print(cpu_count())
    with Pool(4) as p:
        it = p.imap(f, range(5),chunksize=4)
        for i in it:
            print(i,end=' ')

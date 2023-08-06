import time
import sys


class ProgresBar:
    def __init__(self, total_length):
        self.real_length = 40
        self.total_length = total_length
        self.c = self.real_length / total_length
        self.tmp = 0

    def increment(self):
        self.tmp += 1
        if self.tmp <= self.total_length:
            p = int(self.c * self.tmp)
            p_ = self.real_length - p
            str_bar = '\rProgress [' + '#' * p + '-' * p_ + ']'
            str_p = self.tmp / self.total_length
            str_all = str_bar + f'\t{str_p:{3}.{1}%}' + f'\t[{self.tmp}/{self.total_length}]'
            print(str_all, end='')


if __name__ == '__main__':
    bar = ProgresBar(145)
    for i in range(165):
        time.sleep(0.02)
        bar.increment()

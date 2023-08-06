import hashlib
import pickle
from typing import *
import os


class cache:
    """将一个函数的结果储存
        Note:
            pass
        Args:
            fnc (function): 被调用的函数
        Example:
                @cache
                def foo(x):
                    for i in range(10):
                        i *= (i + 1)
                    return i
    """

    def __init__(self, fnc: Callable):
        self.fnc = fnc
        self.fnc_name = self.fnc.__name__

    def __call__(self, *args, **kwargs):
        sha = hashlib.sha256()
        sha.update(pickle.dumps((self.fnc_name, args, frozenset(kwargs.items()))))
        out_path = os.path.join('.cache', f'{sha.hexdigest()}_{self.fnc_name}')
        try:
            with open(out_path, 'rb') as f:
                data = pickle.load(f)
        except FileNotFoundError:
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            data = self.fnc(*args, **kwargs)
            with open(out_path, 'wb') as f:
                pickle.dump(data, f)
        return data


if __name__ == '__main__':
    @cache
    def foo(x):
        for i in range(x):
            i *= (i + 1)
        return i


    print(foo(10))
    print(foo(101))

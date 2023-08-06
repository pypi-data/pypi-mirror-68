import time


# 装饰其第一种写法
# def timer(f):
#     def __wrapper(*args, **kwargs):
#         time_start = time.time()
#         result = f(*args, **kwargs)
#         time_end = time.time()
#         print(f'func:{f.__name__!r}  took: {time_end - time_start:{7}.{6}} sec')
#         return result
#
#     return __wrapper

# 装饰其第二种写法
class timer:
    """ 计算一个函数的执行时间
        Note:
            无
        Args:
            fnc (function): fucntions to be called.
        Example:
            ::
                @timer
                def foo(x):
                    for i in range(x):
                        time.sleep(0.01)
        """
    def __init__(self, fnc):
        self.fnc = fnc

    def __call__(self, *args, **kwargs):
        time_start = time.time()
        self.fnc(*args, **kwargs)
        time_end = time.time()
        print(f'func:{self.fnc.__name__!r}  took: {time_end - time_start:{7}.{6}} sec')


if __name__ == '__main__':

    @timer
    def foo(x):
        for i in range(x):
            time.sleep(0.01)


    foo(100)

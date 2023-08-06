class EasyDict(dict):

    def __init__(self, d=None, **kwargs):
        if d is None:
            d = {}
        for k, v in d.items():
            setattr(self, k, v)

    def __setattr__(self, name, value):
        if isinstance(value, dict):
            value = self.__class__(value)
        super(EasyDict, self).__setattr__(name, value)
        super(EasyDict, self).__setitem__(name, value)


if __name__ == '__main__':
    d = EasyDict({'foo': 3, 'bar': {'x': 1, 'y': 2}})
    dp = d.foo
    x = d.bar.x
    dp1 = d['foo']
    x1 = d['bar']['x']
    a = 1

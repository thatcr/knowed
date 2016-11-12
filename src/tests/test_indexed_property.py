from pytest import raises

class IndexedPropertyMapper(object):
    def __init__(self, desc, instance):
        self.desc = desc
        self.instance = instance

    def __getitem__(self, item):
        return self.desc.fget(self.instance, item)

    def __setitem__(self, item, value):
        # hmm. is this order of arguments right?
        self.desc.fset(self.instance, value, item)

    def __delitem__(self, item):
        self.desc.fdel(self.instance, item)

class MultiIndexedPropertyMapper(object):
    def __init__(self, desc, instance):
        self.desc = desc
        self.instance = instance

    def __getitem__(self, item):
        return self.desc.fget(self.instance, *item)

    def __setitem__(self, item, value):
        # hmm. is this order of arguments right?
        self.desc.fset(self.instance, *item, value)

    def __delitem__(self, item):
        self.desc.fdel(self.instance, *item)

# could we allow __delete__ to invalidate all nodes?
# what does __set__ do? assign the whole mapping? that sounds ok.
# can we assign slices -> translate to multipl set calls?  but we don't know.

class IndexedPropertyDescriptor(property):
    def __get__(self, instance, owner):
        return IndexedPropertyMapper(self, instance)


class MultiIndexedPropertyDescriptor(property):
    def __get__(self, instance, owner):
        return MultiIndexedPropertyMapper(self, instance)

def index(fget, *args, **kwargs):

    if fget.__code__.co_argcount > 2:
        return MultiIndexedPropertyDescriptor(fget, *args, **kwargs)
    if fget.__code__.co_argcount == 2:
        return IndexedPropertyDescriptor(fget, *args, **kwargs)
    raise ValueError('index property must take at least one parameter')

def test_indexed_property():
    class Thingy(object):
        @index
        def AddOne(self, i):
            return i + 1

        @index
        def AddTwo(self, i, j):
            return i+j

    t = Thingy()

    with raises(AttributeError):
        t.AddOne = 123

    with raises(AttributeError):
        del t.AddOne

    assert t.AddOne[1] == 2
    assert t.AddOne[3] == 4
    assert t.AddTwo[2,3] == 5


class FibonacciThingy(object):
    @index
    def Fib(self, item):
        if item < 0:
            raise KeyError('must be bigger than 0')
        if item == 0 or item == 1:
            return 1
        return self.Fib[item - 1] + self.Fib[item - 2]

    def method_fib(self, item):
        if item < 0:
            raise KeyError('must be bigger than 0')
        if item == 0 or item == 1:
            return 1
        return barefaced_fib(item - 1) + barefaced_fib(item - 2)

def test_fibonacci():
    t = FibonacciThingy()

    with raises(KeyError):
        t.Fib[-100]

    assert t.Fib[0] == 1
    assert t.Fib[1] == 1
    assert t.Fib[6] == 13


def test_benchmark_fibonacci(benchmark):
    t = FibonacciThingy()
    benchmark(lambda : t.Fib[20])
    assert False

def barefaced_fib(item):
    if item < 0:
        raise KeyError('must be bigger than 0')
    if item == 0 or item == 1:
        return 1
    return barefaced_fib(item - 1) + barefaced_fib(item - 2)

def test_benchmark_barefaced_fib(benchmark):
    benchmark(lambda : barefaced_fib(20))

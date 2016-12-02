from pytest import raises
from functools import wraps
from inspect import signature

# slight improvement: use signature object to bind args and get a key, but _much_ slower: 14us/call
def node(fn):
    __cache__ = {}
    sig = signature(fn)

    print(sig)

    @wraps(fn)
    def _wrapped(*args, **kwargs):
        key = tuple(sig.bind(*args, **kwargs).arguments.items())
        if key in __cache__:
            return __cache__[key]
        value = fn(*args, **kwargs)
        __cache__[key] = value
        return fn(*args, **kwargs)
    _wrapped.__cache__ = __cache__
    return _wrapped

@node
def my_function(a, b, c=None):
     if c:
         return c
     return a + b


def test_thingy():
    assert my_function(1, 2, 3) == 3
    assert my_function(1, 2, c=3) == 3
    assert my_function(1, 2) == 3

    with raises(TypeError):
        assert my_function(1)

    print(my_function.__cache__)


def test_benchmark_thingy(benchmark):
    def _bench():
        assert my_function(1, 2, c=3) == 3

    benchmark(_bench)
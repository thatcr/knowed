from .. import nowd, NowdObject, DictScope
import inspect

class ArguedThing(NowdObject):

    @nowd
    def Normal(self):
        return 1

    @nowd
    def WithArgs(self, a, b, c):
        return a + b + c

    @nowd
    def Fib(self, x : int):
        if x < 0:
            raise ValueError('cannot compute fib on negative numbers')
        if x == 0 or x == 1:
            return 1
        return self.Fib(x-1) + self.Fib(x-2)


def test_args():
    t = ArguedThing()
    assert t.Normal == 1

    assert t.WithArgs(1, 2, 3) == 1 + 2 + 3

    assert t.Fib(0) == 1
    assert t.Fib(1) == 1
    assert t.Fib(2) == 2
    assert t.Fib(3) == 3

# TODO should objects createds in a scope be cached there (and only there?)

def test_args_dict():

    with DictScope() as scope:
        t = ArguedThing()
        assert t.Normal == 1
        assert t.WithArgs(1, 2, 3) == 1 + 2 + 3

        assert t.Fib(0) == 1
        assert t.Fib(1) == 1
        assert t.Fib(2) == 2
        assert t.Fib(3) == 3

    # scope is now a built graph... we can compile it.

    # argument descriptor just returns a function that resolves the cache
    assert inspect.isfunction(scope.cache[t, ArguedThing.WithArgs])

    assert hasattr(ArguedThing.WithArgs, 'Args')
    assert hasattr(ArguedThing.Fib, 'Args')

    #
    # # what do we cache on:
    # keep the object part as the ojbect, but manipulate the desc bit
    # this is better for querying?

    pass

#  are args important enough to warrant 3-tuples?
#  no, we'd still have to resolve



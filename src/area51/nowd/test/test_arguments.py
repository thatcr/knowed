from pytest import raises
from .. import node, NodeBase, DictScope
import inspect

class ArguedThing(NodeBase):

    @node
    def Normal(self):
        return 1

    @node
    def WithArgs(self, a, b, c):
        return a + b + c

    @node
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

    assert inspect.isfunction(scope.cache[t, ArguedThing.WithArgs])

    assert hasattr(ArguedThing.WithArgs, 'Args')
    assert hasattr(ArguedThing.Fib, 'Args')

    with raises(ValueError):
        assert t.Fib(-1)




from pytest import raises

from .. import node, NodeBase, LoggingScope

class FibThing(NodeBase):
    @node
    def Fib(self, x):
        if x < 0:
            raise ValueError('cannot calculate fib < 0')
        if x == 0 or x == 1:
            return 1
        return self.Fib(x-1) + self.Fib(x-2)

def test_args_fib():
    thing = FibThing()
    with LoggingScope():
        with raises(ValueError):
            thing.Fib(-1)

        assert thing.Fib(0) == 1
        assert thing.Fib(1) == 1
        assert thing.Fib(2) == 2
        assert thing.Fib(3) == 3


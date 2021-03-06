from area51.namd import NamdObject
from .. import node, NodeBase
from .. import NullScope, DictScope, LoggingScope
from pytest import raises
class FibThing(NamdObject, NodeBase):
    def __init__(self, x):
        super().__init__(x)
        if x < 0:
            raise ValueError('cannot calculate Fib < 1')
        self.x = x

    @node
    def Fib(self):
        if self.x == 0 or self.x == 1:
            return 1
        return FibThing(self.x-1).Fib + FibThing(self.x-2).Fib

def test_fib():
    with LoggingScope():
        assert FibThing(0).Fib == 1
        assert FibThing(1).Fib == 1
        assert FibThing(2).Fib == 2
        assert FibThing(3).Fib == 3

    with raises(ValueError):
        FibThing(-1).Fib



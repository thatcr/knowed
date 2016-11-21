from .. import nowd, NowdObject

# should we auto detect the arguments node, so @node is our onl decorator
# KIS @stored
# what would the 'indexed' version look like: or is that just a dict with nodes on it's __getitem__
# fo.Index <- normal node attached to the object, returns object then is also a NowdDictionary, where __getitem__ is
# accessed through a dscriptor: does that work for dunder methods? or do we have to treat getitem and setitem
# specially. can it work on regular dicts?

class ArguedThing(NowdObject):

    @nowd()
    def Normal(self):
        return 1

    @nowd(args=True)
    def WithArgs(self, a, b, c):
        return a + b + c

    @nowd(args=True)
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

#  are args important enough to warrant 3-tuples?
#  no, we'd still have to resolve



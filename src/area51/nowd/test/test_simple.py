from pytest import raises

from .. import node, NodeBase, NullScope, DictScope

# get this working before implementing the argument basd nodes.

class Thing(NodeBase):
    @node
    def Leaf(self):
        return 123.123

    @node
    def Node(self):
        return self.Leaf + self.Leaf

def test_fail():
    thing = Thing()

    assert thing.Leaf == 123.123

    with raises(AttributeError):
        thing.Leaf = 256.256

def test_null():
    thing = Thing()
    with NullScope():
        assert thing.Leaf == 123.123
        assert thing.Node == 123.123 + 123.123

        with raises(AttributeError):
            thing.Leaf = 256.256
        assert thing.Leaf == 123.123
        assert thing.Node == 123.123 + 123.123


def test_dict():
    thing = Thing()

    with DictScope() as scope:
        assert thing.Leaf == 123.123
        assert thing.Node == 123.123 + 123.123

    assert scope.cache[thing, Thing.Leaf] == 123.123
    assert scope.cache[thing, Thing.Node] == 123.123 + 123.123

    with DictScope() as scope:
        assert thing.Leaf == 123.123
        assert thing.Node == 123.123 + 123.123

        thing.Leaf = 100
        assert thing.Node == 100 + 100

    assert scope.cache[thing, Thing.Leaf] == 100
    assert scope.cache[thing, Thing.Node] == 100+100



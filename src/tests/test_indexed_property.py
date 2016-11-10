from pytest import raises

class IndexedPropertyMapper(object):
    def __init__(self, desc, instance):
        self.desc = desc
        self.instance = instance

    def __getitem__(self, item):
        return self.desc.fget(self, item)

    def __setitem__(self, item, value):
        # hmm. is this order of arguments right?
        self.desc.fset(self, value, item)

    def __delitem__(self, item):
        self.desc.fdel(self, item)

class MultiIndexedPropertyMapper(object):
    def __init__(self, desc, instance):
        self.desc = desc
        self.instance = instance

    def __getitem__(self, item):
        return self.desc.fget(self, *item)

    def __setitem__(self, item, value):
        # hmm. is this order of arguments right?
        self.desc.fset(self, *item, value)

    def __delitem__(self, item):
        self.desc.fdel(self, *item)

# could we allow __delete__ to invalidate all nodes?
# what does __set__ do? assign the whole mapping? that sounds ok.
# can we assign slices -> translate to multipl set calls?  but we don't know.

class IndexedPropertyDescriptor(property):
    def __get__(self, instance, owner):
        return IndexedPropertyMapper(self, instance)


class MultiIndexedPropertyDescriptor(property):
    def __get__(self, instance, owner):
        return MultiIndexedPropertyMapper(self, instance)

def indexed_property(fget, *args, **kwargs):

    if fget.__code__.co_argcount > 2:
        return MultiIndexedPropertyDescriptor(fget, *args, **kwargs)
    if fget.__code__.co_argcount == 2:
        return IndexedPropertyDescriptor(fget, *args, **kwargs)
    raise ValueError('index property must take at least one parameter')

def test_indexed_property():
    class Thingy(object):
        @indexed_property
        def AddOne(self, i):
            return i + 1

        @indexed_property
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



from weakref import WeakValueDictionary
class IdentifiedMetaClass(type):
    def __new__(meta, name, bases, nmspc):
        nmspc['__cache__'] = WeakValueDictionary()
        # need to manipulate __init__ so that it isn't called twice
        # when we retrieve from the cache, but how to avoid inheritance
        return super().__new__(meta, name, bases, nmspc)

    def __call__(cls, *args):
        instance = cls.__cache__.get(args, None)
        if instance:
            return instance
        instance = super().__call__(cls, *args)
        cls.__cache__[args] = instance
        return instance

class IdentifiedBase(object, metaclass=IdentifiedMetaClass):
    pass

class TrialIdentified(IdentifiedBase):
    def __init__(self, *args):
        assert not hasattr(self, 'done')
        self.done = True

    def foo(self):
        pass

def test_identified():
    x = TrialIdentified('fish')
    y = TrialIdentified('fish')

    assert x is y
    assert x is not TrialIdentified('fish', 'chaps')

    assert TrialIdentified('foo', 'bar') is TrialIdentified('foo', 'bar')



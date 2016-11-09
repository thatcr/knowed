

class IdentifiedMetaClass(type):
    def __new__(meta, name, bases, nmspc):
        nmspc['__cache__'] = {}
        # need to manipulate __init__ so that it isn't called twice
        # when we retrieve from the cache, but how to avoid inheritance
        return super().__new__(meta, name, bases, nmspc)

class IdentifiedBase(object, metaclass=IdentifiedMetaClass):
    def __new__(cls, *args):
        instance = cls.__cache__.get(args, None)
        if args:
            return instance
        instance = super().__new__(cls)
        cls.__cache__[args] = instance
        return instance


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



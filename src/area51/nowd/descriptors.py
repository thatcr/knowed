from area51.namd import NamdObject
from .base import NowdScope

#  should we use inhertance on Nowd instead: base class manages the scope
#  and cache: problem is that the fget isn't really a valid fget in a lot of cases.

#  keep cache clea
#  desc.__get__ on Args, should use the arg values !

class NowdDescriptor(property):
    def __repr__(self):
        return self.fget.__code__.co_name

class ArgsDescriptor(NamdObject, property):
    def __init__(self, desc, *args):
        super().__init__(desc, *args)
        self.desc = desc
        self.args = args

    def __get__(self, instance, owner=None):
        return self.desc.fget(instance, *self.args)

# Args can be more expressive.
class ArgsNowdDescriptor(property):

    def __repr__(self):
        return self.__class__.__name__

    def __get__(self, instance, owner=None):
        # important to do this else class attribute access ends on graph also.
        if instance is None:
            return super().__get__(instance, owner)

        # otherwise it's a normal propery get, make a binder that routes
        # to the context (should be an object with __call__)
        def _bound(*args):
            return NowdScope.context[instance, ArgsDescriptor(self, *args)]

        return _bound


    def __set__(self, instance, value):
        raise NotImplementedError

nowd=NowdDescriptor

def nowd(args=None):
    if args is None:
        return NowdDescriptor
    else:
        return ArgsNowdDescriptor



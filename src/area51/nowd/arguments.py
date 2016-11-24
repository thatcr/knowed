from area51.namd import NamdObject
from .scopes import Scope


class ArgsDescriptorArgs(NamdObject, property):
    def __init__(self, desc, *args):
        super().__init__(desc, *args)
        self.desc = desc
        self.args = args

    def __get__(self, instance, owner=None):
        return self.desc.fget(instance, *self.args)

    def __repr__(self):
        return "{self.desc!r}{self.args!r}".format(self=self)

class ArgsDescriptorMetaClass(type):
    """
    create an arg class wrapper unique to this descriptor type - this means that the Args
    class will get it's own cache of arguments particular to the desctipor which should
    reduce the size of the cache to be only those args used on that particular descriptor.
    """
    def __new__(meta, name, bases, nmspc):
        nmspc['Args'] = type('Args', (ArgsDescriptorArgs,), {})
        return super().__new__(meta, name, bases, nmspc)

# Args can be more expressive.
class ArgsDescriptor(property, metaclass=ArgsDescriptorMetaClass):
    def __get__(self, instance, owner=None):
        # important to do this else class attribute access ends on graph also.
        if instance is None:
            return super().__get__(instance, owner)

        # otherwise it's a normal property get, make a binder that routes
        # to the context (should be an object with __call__)
        def _bound(*args):
            return Scope.context[instance, self.__class__.Args(self, *args)]

        return _bound

    def __repr__(self):
        return self.__class__.__name__

    def __set__(self, instance, value):
        raise NotImplementedError

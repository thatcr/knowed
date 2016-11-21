from .meta import NamdClass

'''
NOTE the types of __init__ can be used to generate an autocomplete + grammar for resolving items:
    if we have a sequenceof class, values we can complete lexeme tokens and a grammar with ply

TODO turn kwargs into a mush, so args map to clean strings, kwags to some hash (careful with dict ordering)
     what is an acceptable collisiotn on mush? can we re-mush other object names (bad).

     do we need to store a weakref dict of instances?


'''

class NamdObject(object, metaclass=NamdClass):
    def __init__(self, *args):
        super().__init__()
        self.__init_args__ = args

    def __repr__(self):
        return "{self.__module__!s}.{self.__class__.__name__!s}{self.__init_args__!r}".format(self=self, )

    def __str__(self):
        if not self.__args__:
            return self.__class__.__name__
        return "{self.__class__.__name__!s} {args}".format(self=self, args=' '.join(map(str, self.__init_args__)))
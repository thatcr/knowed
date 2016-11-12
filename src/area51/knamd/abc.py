from .meta import KnamedClass

'''
NOTE the types of __init__ can be used to generate an autocomplete + grammar for resolving items:
    if we have a sequenceof class, values we can complete lexeme tokens and a grammar with ply



'''

class KnamedObject(object, metaclass=KnamedClass):
    def __init__(self, *args):
        self.__args__ = args

    def __repr__(self):
        return "{self.__module__!s}.{self.__class__.__name__!s}{self.__args__!r}".format(self=self, )

    def __str__(self):
        if not self.__args__:
            return self.__class__.__name__
        return "{self.__class__.__name__!s} {args}".format(self=self, args=' '.join(map(str, self.__args__)))
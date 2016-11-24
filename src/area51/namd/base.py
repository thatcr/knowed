from .meta import NamdClass


class NamdObject(object, metaclass=NamdClass):
    def __init__(self, *args):
        super().__init__()
        self.__init_args__ = args

    def __repr__(self):
        return "{self.__module__!s}.{self.__class__.__name__!s}{self.__init_args__!r}".format(self=self, )

    def __str__(self):
        if not self.__init_args__:
            return self.__class__.__name__
        return "{self.__class__.__name__!s} {args}".format(self=self, args=' '.join(map(str, self.__init_args__)))
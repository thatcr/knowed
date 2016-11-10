
class KnamedClass(type):
    def __new__(meta, name, bases, nmspc):
        '''
        adds a class level __cache__ member to store instances of this type
        :param name:
        :param bases:
        :param nmspc:
        :return:
        '''
        nmspc['__cache__'] = dict()
        return super().__new__(meta, name, bases, nmspc)

    def __call__(cls, *args):
        '''
        retrieve instance from the cache if one has already been created with the same arguments

        At the moment we only support unnamed arguments - kwargs being a dict is unhelpful when computing
        the cache key. Future versions of python may vary, or we'll apply a frozendict.
        :param args: complete arguments to the function
        :return: object instance from cache, or newly created if not seen before
        '''
        instance = cls.__cache__.get(args, None)
        if instance:
            return instance
        instance = super().__call__(*args)
        cls.__cache__[args] = instance
        return instance
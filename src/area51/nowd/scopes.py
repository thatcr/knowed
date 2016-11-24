import logging

from collections import defaultdict

class Scope(object):
    _stack = []

    def __enter__(self):
        Scope._stack.append(Scope.context)
        assert self not in Scope._stack, 'context is already on the stack'
        Scope.context = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Scope.context = Scope._stack.pop()

    def __getitem__(self, item):
        instance, desc = item
        return desc.__get__(instance)

    def __setitem__(self, item, value):
        instance, desc = item
        return desc.__set__(instance, value)

Scope.context = Scope()

class NullScope(Scope):
    def __getitem__(self, item):
        obj, desc = item
        return desc.__get__(obj)

    def __setitem__(self, item, value):
        obj, desc = item
        return desc.__set__(obj, value)

class LoggingScope(NullScope):
    def __init__(self, log=logging):
        super().__init__()
        self.indent = 0
        self.log = log

    def __getitem__(self, item):
        self.log.debug('GET ' + self.indent * '..' + repr(item))
        self.indent += 1
        try:
            return super().__getitem__(item)
        finally:
            self.indent -= 1

    def __setitem__(self, item, value):
        self.log.debug('SET {!r} = {!r}'.format(item, value))
        return super().__setitem__(item, value)

class DictScope(Scope):
    def __init__(self, cache_type=dict):
        self.cache = cache_type()
        self.stack = []
        self.dependents = defaultdict(set)

    def __getitem__(self, item):
        obj, desc = item

        if self.stack:
            self.dependents[item].add(self.stack[-1])
        self.stack.append(item)
        try:
            if item in self.cache:
                return self.cache[item]
            value = desc.__get__(obj)
            self.cache[item] = value
            return value
        finally:
            self.stack.pop()

    def __setitem__(self, item, value):
        assert not self.stack, 'attempted to set node as part of an evaluation'

        obj, desc = item

        # evict everything from the cache with this node as a parent
        dependents = [item]
        for dependent in dependents:
            logging.debug('FOR {!r}'.format(dependent))
            dependents.extend(self.dependents.pop(dependent, []))
            self.cache.pop(dependent, None)

        self.cache[item] = value

        # TODO how do we interact with __setitem__ here?

    # convert nodes -> dict for pformatting?
    def to_log(self, logger):
        for key, value in self.items():
            logger.info('CACHE {key[0]!r}.{key[1]!r} = {value!r}'.format(key=key, value=value))

        for key, value in self.dependents.items():
            logging.info('{key[0]!r}.{key[1]!r}'.format(key=key))
            for parent in value:
                logger.info('   < {key[0]!r}.{key[1]!r}'.format(key=parent))

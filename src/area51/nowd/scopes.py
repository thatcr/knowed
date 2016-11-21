import logging
from .abc import NowdScope
from collections import defaultdict

class NullScope(NowdScope):
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
        self.logger.debug('GET ' * self.indent * '..' + repr(item))
        self.indent += 1
        try:
            return super().__getitem__
        finally:
            self.indent -= 1

    def __setitem__(self, item, value):
        self.logger.debug('SET {!r} = {!r}'.format(item, value))

class DictScope(NowdScope):
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

        # now just set it via the descriptor, we don't need this on-graph yet
        # don't: if we are in a scope we're overriding values?
        # in order to set we have to 'escape' the scope: push a NullContext?
        # desc.__set__(obj, value)

    # convert nodes -> dict for pformatting?
    def to_log(self, logger):
        for key, value in self.items():
            logger.info('CACHE {key[0]!r}.{key[1]!r} = {value!r}'.format(key=key, value=value))

        for key, value in self.dependents.items():
            logging.info('{key[0]!r}.{key[1]!r}'.format(key=key))
            for parent in value:
                logger.info('   < {key[0]!r}.{key[1]!r}'.format(key=parent))

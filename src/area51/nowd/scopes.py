import logging

from collections import defaultdict

# protocol: should we allow __delitem__ to signify an invalidation
#           and have __setitem__ just set afterwards.
#           that would allow combining the node caching strategy and dependneices easier
#           do we want to allow the descriptor to hook the invalidation?
#           the scope is enough:

# TODO how does the underlying descriptor protocol work against __dict__ when we are
#      not inside a node:
#      __get__: _returns_ a calculated node value
#      __set__: does this modify something in __dict__? can it be called from within a scope.
#      __del__: removes a node from the object

# is there any need to conflate this with the node stuff? or is it completely separate
# __get__ is the on-graph bit. should we avoid overridding it ? have a __node__
# function instead that __get__ defers to ? differing versions on/off graph?
# or is that not necessary:
# if we SET/DEL on-graph, what does that mean?
# does it reassign a node common to all scopes, in the base scope - hard, as we have to invalidate all active scopes
# or does it just modify the existing graph - safter
# when in a NullScope, anything @Stored works against the __dict__.
# cleanly seperate the modes of operation: non-graph when simpky updating tradable values, and computing @Get.
# graphed when doing calculations (like QT).
#
# QT special case if we commit we need to transfer values from the graph ones to the __dict__
#  what's the mechanism? i.e. commit(security, scope) - update security from node values in scope
# QT really needs to store entire graph, so it's not relevant.

# is there scope for replacing __dict__ with an on-graph __dict__?
# that allows the get/set to be kept in place: entire object state moves on graph
# just need the DictBase object and storage to work, then we can try.
#
# do we have any concept of a node shared between scopes like this. makes the invalidate stuff hard, unless we
# keep a stack of active scopes.





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

    def __delitem__(self, item):
        instance, desc = item
        return desc.__delete__(instance)

Scope.context = Scope()

class NullScope(Scope):
    pass

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

    def __delitem__(self, item):
        self.log.info('DEL {!r}'.format(item))
        return super().__delitem__(item)

    def __setitem__(self, item, value):
        self.log.info('SET {!r} = {!r}'.format(item, value))
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

    def __delitem__(self, item):
        assert not self.stack, 'attempted to del node as part of an evaluation'

        # evict everything from the cache with this node as a parent
        dependents = [item]
        for dependent in dependents:
            logging.debug('DEL {!r}'.format(dependent))
            dependents.extend(self.dependents.pop(dependent, []))
            self.cache.pop(dependent, None)

    def __setitem__(self, item, value):
        assert not self.stack, 'attempted to set node as part of an evaluation'

        # invalidate first
        self.__delitem__(item)
        self.cache[item] = value


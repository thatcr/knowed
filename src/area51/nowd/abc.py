import threading

# reconsider this: the context behvaiour should move to the __getattr__?
# nodeobject might detect __dict__ access on-graph, and break?
# how about globals()?

# scope behaviour: should we pass through to __set__, or keep it in the dict ?
#    basic scope would use set?
#    should a node have any set function at all: but always rely on the scope
#    or is the NullScope behaviour accurate: set should store, and just work.

class NowdObject(object):
    def __getattribute__(self, item):
        desc = getattr(super().__getattribute__('__class__'), item, None)
        if isinstance(desc, property):
            return NowdScope.context[self, desc]
        return super().__getattribute__(item)

    def __setattr__(self, item, value):
        desc = getattr(super().__getattribute__('__class__'), item, None)
        if isinstance(desc, property):
            # should we stack up contexts here? or use the same one?
            NowdScope.context[self, desc] = value
            return
        return super().__setattr__(self, item, value)

class NowdScope(object):
    _stack = []

    def __enter__(self):
        NowdScope._stack.append(NowdScope.context)
        assert self not in NowdScope._stack, 'context is already on the stack'
        NowdScope.context = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        NowdScope.context = NowdScope._stack.pop()

    def __getitem__(self, item):
        raise NotImplementedError

    def __setitem__(self, item, value):
        raise NotImplementedError

NowdScope.context = NowdScope()
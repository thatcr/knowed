from .scopes import NowdScope

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
        return super().__setattr__(item, value)
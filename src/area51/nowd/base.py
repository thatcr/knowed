from .scopes import Scope

class NowdObject(object):
    '''
    this object redirects getattribute and setattr on descriptors through to the
    node context.
    '''
    def __getattribute__(self, item):
        desc = getattr(super().__getattribute__('__class__'), item, None)
        if isinstance(desc, property):
            return Scope.context[self, desc]
        return super().__getattribute__(item)

    def __setattr__(self, item, value):
        desc = getattr(super().__getattribute__('__class__'), item, None)
        if isinstance(desc, property):
            # should we stack up contexts here? or use the same one?
            Scope.context[self, desc] = value
            return
        return super().__setattr__(item, value)
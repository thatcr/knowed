
# how do we represnet nodes with argumnets: assignment syntax is awkwards
class NowdDescriptor(property):
    def __repr__(self):
        return self.fget.__code__.co_name

class ArgsNowdDescriptor(property):
    def __repr__(self):
        return self.__class__.__name__

nowd=NowdDescriptor

def nowd(args=None):
    if args is None:
        return NowdDescriptor
    else:
        return ArgsNowdDescriptor



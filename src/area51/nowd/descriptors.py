from area51.namd import NamdObject
from .base import NowdScope

class NowdDescriptor(property):
    def __repr__(self):
        return self.fget.__code__.co_name

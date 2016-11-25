import inspect

from .descriptors import Descriptor
from .arguments import ArgsDescriptor

def node(fget, *args, **kwargs):
    signature = inspect.signature(fget)

    base = ArgsDescriptor if len(signature.parameters) > 1 else Descriptor
    cls = type(fget.__code__.co_name + 'Descriptor', (base, ), {})

    return cls(fget, *args, **kwargs)
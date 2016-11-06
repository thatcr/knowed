from collections import OrderedDict
from inspect import isgeneratorfunction
import logging
import threading

logging.basicConfig(level=logging.DEBUG)

node_context = threading.local()

class LoggingContext(object):
    indent = 0
    def __init__(self, obj, desc):
        self.obj = obj
        self.desc = desc

    def __enter__(self):
        logging.debug('    ' * self.indent + repr((self.obj, self.desc)))
        self.__class__.indent += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__class__.indent -= 1

node_context.context = LoggingContext

# how do we represnet nodes with argumnets: assignment syntax is awkwards

'''
foo.Currency['x', 1, 2]  =
foo.Currency['x', 3, 4]

__getitem__, __setitem__, __delitem__

use slice syntax? allow for mnulticalls with slicing, nicely?

'''

'''
better way

-  need objects to be singleone on __new__, with avoided __init_, soo x('A") is x('A'),
- the we have a better equivalence for caching:


- remap the Thing call into an object with a property of that name.
def Thing(self, arg1, arg2):
    ....

- ThingCaller(self, arg1, arg2).Thing

THat means that the cache still only deals with object, descriptor as keps/values of nodes.
The name resolution logic sits in the getter. But we have to remmeber the sets of argumenst that were invoked.

- Or a better syntax?

self[arg1, arg2].Thing

- define a cached space of called object with arguments,

'''

class NodeMetaClass(type):
    def __new__(cls, name, bases, nmspc):
        # translate any node descriptors into distinct types
        for key, value in nmspc.items():
            if not isinstance(value, property):
                continue
            # what it the value is a node descriptor from _another_ class? do we make our own...
            # getters on that will get an unexpected instance, which may be ok

            nmspc[key] = type(key + 'Descriptor', (property,), {})(
                fget=value.fget, fset=value.fset, fdel=value.fdel, doc=value.__doc__
            )

        return super().__new__(cls, name, bases, nmspc)

class NodeBase(object, metaclass=NodeMetaClass):
    trace = [[]]

    def __getattribute__(self, item):
        desc = getattr(super().__getattribute__('__class__'), item, None)
        if isinstance(desc, property):
            # should we stack up contexts here? or use the same one?
            with node_context.context(self, desc):
                return super().__getattribute__(item)
        else:
            return super().__getattribute__(item)


node = property

class Cash(NodeBase):
    @node
    def Currency(self) -> str:
        '''this is a 'defaulter' and returns the value represented by the node if not set'''
        return self.__dict__.get('Currency', 'EUR')

    @Currency.setter
    def Currency(self, value : str):
        '''this is a resolver, and translates the value specified to an internal representation'''
        if value not in {'EUR', 'USD'}:
            raise ValueError('invalid currency {}'.format(value))
        self.__dict__['Currency'] = value

    @node
    def Quantity(self) -> float:
        return self.__dict__.get('Quantity', 1.0)

    @Quantity.setter
    def Quantity(self, value : float):
        if value <= 0.0:
            raise ValueError('quantity must b greater than 0')
        self.__dict__['Quantity'] = value

    @node
    def Price(self):
        return self.Quantity * (1.0 if self.Currency == 'USD' else 0.5)

    @node
    def DollarPrice(self):
        return self.Price / (1.0 if self.Currency == 'USD' else 0.5)

def test_cash():
    c = Cash()

    assert c.Price == 0.5
    c.Currency = 'USD'
    c.Quantity = 100.0

    assert c.Price == 100.0

    c.Currency = 'EUR'
    assert c.Price == 50.0

    assert c.DollarPrice == 100.0


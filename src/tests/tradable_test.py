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


class FunctionNodeDescriptor(object):
    trace = [[]]
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.doc = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")

        self.trace[-1].append((obj, self))
        self.trace.append([])

        with node_context.context(obj, self):
            return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

    def __repr__(self):
        return self.__class__.__name__

class TradableMetaClass(type):
    def __new__(cls, name, bases, nmspc):
        # translate any node descriptors into distinct types
        for key, value in nmspc.items():
            if not isinstance(value, property):
                continue
            # what it the value is a node descriptor from _another_ class? do we make our own...
            # getters on that will get an unexpected instance, which may be ok

            nmspc[key] = type(key + 'Descriptor', (FunctionNodeDescriptor,), {})(
                fget=value.fget, fset=value.fset, fdel=value.fdel, doc=value.__doc__
            )

        return super().__new__(cls, name, bases, nmspc)

node = property

class Cash(metaclass=TradableMetaClass):
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


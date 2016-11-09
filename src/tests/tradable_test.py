import sys
import logging
import threading
from collections import defaultdict
import networkx as nx
from pprint import pformat

logging.basicConfig(level=logging.DEBUG)

node_context = threading.local()

# TODO replace the 2-tuple with something that repres nicely: a BoundDesc (are boundfuncs the same? )
# TODO implement named object defined by the cache of their init functions
# TODO re-use that to implement the Args(...) idea for properties with multiple values
# TODO how do we expose args? We really want named args.
# TODO Args objects are cached on the object itself and return the same thing based upon the
#      the arguments and the object instance. THey then cache the VTs on tha tobject.
'''
    obj.PriceWhen(123, X=0)
    obj.PriceWhen(123, X=0) < won't ever work
    obj.PriceWhen[123, X=0] < won't work, no named.
    obj.PriceWHen[123, X=0] = 123, but that works. trailing dict is kwargs? or enforce kwargs.

    obj.__args__(123, X=0).PriceWhen = foo # ok but clunky

    the [] syntax works nicely, could also extend to ranges or arguments, but prevens any named arguments.
    by can alway do
    boj.PriceWhen[{'X'= 0}]

    no escaling the assigment problem.




'''
class TrialContext(dict):

    def __init__(self):
        self.stack = []
        self.indent = 0
        self.parents = defaultdict(set)

    def __getitem__(self, key):
        obj, desc = key
        logging.debug('    GET ' * self.indent + repr((obj, desc)))

        self.indent +=1
        if self.stack:
            self.parents[key].add(self.stack[-1])
        self.stack.append(key)
        try:
            if key in self:
                logging.debug('    ' * self.indent + 'REM {!r}'.format(key))
                return super().__getitem__(key)

            value = desc.__get__(obj)
            super().__setitem__(key, value)
            return value
        finally:
            self.stack.pop()
            self.indent -= 1

    def __setitem__(self, key, value):
        assert self.indent == 0, 'attempted to set node as part of an evaluation'
        logging.debug('SET {!r} = {!r}'.format(key, value))

        # does this vale end up on graph? yes. SetRetain means on graph, but not on object
        # @Stored means put it in the __dict__

        obj, desc = key

        # evict everything from the cache with this node as a parent
        ancestors = [key]
        for ancestor in ancestors:
            logging.debug('FOR {!r}'.format(ancestor))
            ancestors.extend(self.parents.pop(ancestor, []))
            self.pop(ancestor, None)

        # now just set it via the descriptor, we don't need this on-graph yet
        desc.__set__(obj, value)

    def to_log(self, logger):
        for key, value in self.items():
            logging.info('CACHE {key[0]!r}.{key[1]!r} = {value!r}'.format(key=key, value=value))

        for key, value in self.parents.items():
            logging.info('{key[0]!r}.{key[1]!r}'.format(key=key))
            for parent in value:
                logging.info('   < {key[0]!r}.{key[1]!r}'.format(key=parent))


node_context.context = TrialContext()

# how do we represnet nodes with argumnets: assignment syntax is awkwards
class NodeDescriptor(property):
    def __repr__(self):
        return self.__class__.__name__

class NodeMetaClass(type):
    def __new__(cls, name, bases, nmspc):
        # translate any node descriptors into distinct types
        for key, value in nmspc.items():
            if not isinstance(value, property):
                continue
            # what it the value is a node descriptor from _another_ class? do we make our own...
            # getters on that will get an unexpected instance, which may be ok

            nmspc[key] = type(key, (NodeDescriptor,), {})(
                fget=value.fget, fset=value.fset, fdel=value.fdel, doc=value.__doc__
            )

        return super().__new__(cls, name, bases, nmspc)

class NodeBase(object, metaclass=NodeMetaClass):
    '''
    redirect ay access to properties on this class through the node context
    which is a dict indexed by object, descriptor that can capture the node
    evaluation graph and provide cached values
    '''

    def __getattribute__(self, item):
        desc = getattr(super().__getattribute__('__class__'), item, None)
        if isinstance(desc, property):
            return node_context.context[self,desc]
        return super().__getattribute__(item)


    def __setattr__(self, item, value):
        desc = getattr(super().__getattribute__('__class__'), item, None)
        if isinstance(desc, property):
            # should we stack up contexts here? or use the same one?
            node_context.context[self,desc] = value
            return
        return super().__setattr__(self, item, value)

    def __repr__(self):
        return "{!s} @ 0x{:x}".format(self.__class__.__name__, id(self))


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


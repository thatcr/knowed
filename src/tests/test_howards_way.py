

class Attribute(property):
    @classmethod
    def compute():
        ...



class MyInt(Attribute):
    def compute(x : FloatAttribute):
        return int(x) * 2.0

class MyFloat(Attribute):
    def compute():
        return 123.123

class HowardsMetaClass(type):
    # scrape __attributes__ into definition (easy to adapt)
    # what's the difference between attribute and a descriptor?
    pass

class HowardsObject(object, metaclass=HowardsMetaClass):
    def __init__(self):
        super().__init__()
        self.__cache__ = {}

class TestObject(HowardsObject):
    __attributes__ = [ MyInt, MyFloat ]

    @attribute
    def AnotherThing(x: MyInt, y: MyFloat):
        return x + y

o = HowardsObject()

assert o.MyInt == int(123.123 * 2.0)
assert o.AnotherThing == int(123.123 * 2.0) + 123.123

# dependencies are taken from the annotations of the attribute function
# and and a topological orering of the nodes. graph can be build without
# evaluating the compute functions.
#
# once built, just evaluate left to right, filling in the arguments to each call with the right
# values which are guaranteeed to be computed first.

# when you invalidate what happens?
# how do we know which nodes to recompute if all we have is the topological sort?
# I think we are missing some information.

#

# caching/storage is done on the object, so __cache__ is keyed on the node

'''
is this a bit like a compiled graph? first step computes the dependencies, and generates a compute function
then second step runs the evaluation.
'''
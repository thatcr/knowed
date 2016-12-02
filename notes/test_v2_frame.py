# use the stack frame to get the node
import sys

__cache__ = {}
# careful: don't use tracebacks (they are expensive)
#          frames are all we have, but if we have a function wrapper
#          before injecting we can do stuff to link to the function
#  looks like the key construction is the killer: 1us of the call is there.
#
def node():
    d = 4
    frame = sys._getframe().f_back
    key = (frame.f_code.co_name, ) + tuple(frame.f_locals.items())
    return __cache__.get(key, Ellipsis)

# doesn't work! how does the value get back in!

def my_function(a, b, c=None):
    value = node()
    if value is not Ellipsis:
        return value
    if c:
        return c
    return a + b


def test_thingy():
    assert my_function(1,2,3) == 3
    assert my_function(1,3) == 4


def test_benchmark_thingy(benchmark):
    def _bench():
        assert my_function(1, 2, c=3) == 3

    benchmark(_bench)
from area51.namd import NamdObject
from area51.nowd import NowdObject

from pytest import raises
# TODO could we use some getter on __args__ to avoid storing args twice


class FibNowd(NowdObject):
    def __init__(self, arg : int):
        super().__init__()
        if arg < 0:
            raise ValueError('cannot calculate for < 0')
        self.arg = arg

    @property
    def Value(self):
        if self.arg == 0 or self.arg == 1:
            return 1
        return FibNowd(i-1).Value + FibNowd(i-2).Value



def test_fib_nowd():
    assert FibNowd(100) is FibNowd(100)
    assert FibNowd(56).arg == FibNowd(56)

    assert FibNowd(0).Value == 1

    with raises(ValueError):
        FibNowd(-10)

    assert FibNowd(2) == 2
    assert FibNowd(3) == 3
    assert FibNowd(5) == 5






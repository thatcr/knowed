import logging
from .. import node, NodeBase, LoggingScope


class Thing(NodeBase):
    @node
    def Thang(self):
        return 123.123

    @Thang.setter
    def Thang(self, value):
        self.__dict__['Thang'] = value

    @node
    def Thong(self):
        return self.Thang + self.Thang

def test_logging_scope_debug(caplog):
    t = Thing()
    with caplog.at_level(logging.DEBUG):
        with LoggingScope():
            assert t.Thang == 123.123
            assert t.Thong == t.Thang * 2

        assert len(caplog.records) == 5

        assert caplog.records[0].message == 'GET {!r}'.format((t, Thing.Thang))
        assert caplog.records[1].message == 'GET {!r}'.format((t, Thing.Thong))
        assert caplog.records[2].message == 'GET ..{!r}'.format((t, Thing.Thang))
        assert caplog.records[3].message == 'GET ..{!r}'.format((t, Thing.Thang))
        assert caplog.records[4].message == 'GET {!r}'.format((t, Thing.Thang))

def test_logging_scope_info(caplog):
    thing = Thing()
    with caplog.at_level(logging.INFO):
        with LoggingScope():
            thing.Thang = 456.456

    assert caplog.records[0].message == 'SET {!r} = 456.456'.format((thing, Thing.Thang))



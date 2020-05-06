import pytest

from paragraph.NeoGraphDB import NeoGraphDB
from paragraph.interfaces import ObjectDict


@pytest.fixture(scope='session')
def neograph():
    return NeoGraphDB(debug=0)


@pytest.fixture()
def db(neograph):
    yield neograph
    neograph.rollback()


@pytest.fixture()
def testdata(neograph):
    data = ObjectDict()
    data.node = neograph.add_node('Testlabel', foo='bar')
    data.alice = neograph.add_node('Person', name='alice')
    data.bob = neograph.add_node('Person', name='bob')
    data.charlie = neograph.add_node('Person', name='charlie')
    return data

@pytest.fixture()
def linkeddata(neograph, testdata):
    neograph.add_edge(testdata.alice, 'long', testdata.bob)
    neograph.add_edge(testdata.bob, 'long', testdata.charlie)
    neograph.add_edge(testdata.alice, 'short', testdata.charlie)
    return testdata

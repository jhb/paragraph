import pytest

from paragraph.NeoGraphDB import NeoGraphDB
from paragraph.interfaces import ObjectDict


@pytest.fixture(scope='session')
def neograph():
    return NeoGraphDB(debug=0)


@pytest.fixture()
def db(neograph):
    yield neograph
    print('')
    neograph.rollback()


@pytest.fixture()
def testdata(db):
    data = ObjectDict()
    data.db = db
    data.node = data.db.add_node('Testlabel', foo='bar')
    data.alice = data.db.add_node('Person', name='alice')
    data.bob = data.db.add_node('Person', name='bob')
    data.charlie = data.db.add_node('Person', name='charlie')
    yield data


@pytest.fixture()
def linkeddata(testdata):
    db = testdata.db
    db.add_edge(testdata.alice, 'long', testdata.bob)
    db.add_edge(testdata.bob, 'long', testdata.charlie)
    db.add_edge(testdata.alice, 'short', testdata.charlie)
    yield testdata

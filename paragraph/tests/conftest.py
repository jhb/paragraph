import pytest

from paragraph.NeoGraphDB import NeoGraphDB
from paragraph.basic import ObjectDict


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
    data.dora = data.db.add_node('Person', name='dora')
    yield data


@pytest.fixture()
def ld(testdata):
    data = testdata
    db = data.db
    data.e1 = db.add_edge(data.alice, 'long', data.bob)
    data.e2 = db.add_edge(data.bob, 'long', data.charlie)
    data.e4 = db.add_edge(data.alice, 'short', data.charlie)
    data.e3 = db.add_edge(data.charlie, 'long', data.dora)
    yield data

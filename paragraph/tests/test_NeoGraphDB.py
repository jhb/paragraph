import pytest

from paragraph.basic import Node, Edge

def test_create_node(db):
    "Create a node"

    n = db.add_node('Testlabel', foo='bar')
    assert n == {'_id': '...', 'foo': 'bar'}
    assert n.labels == {'Testlabel',}


def test_update_node(db):
    "Update a node"

    n = db.add_node('Testlabel', foo='bar')

    n['foo2'] = 'bar2'
    n.labels.add('Testlabel2')

    n2 = db.update_node(n)
    assert n2 == {'_id':     '...',
                  'foo2':    'bar2',
                  'foo':     'bar'}

    assert n2.labels ==  {'Testlabel2', 'Testlabel'}

def test_query_node(db, testdata):
    "Nodes can be queried"
    r = db.query_nodes(_id=testdata.node.id)
    assert r[0] == testdata.node


def test_delete_node(db):
    "Nodes can be deleted"

    # Lets add another node
    n4 = db.add_node('testnode')

    # Now its there
    r = db.query_nodes(_id=n4.id)
    assert r[0] == n4

    # Now its not...
    db.del_node(n4.id)
    assert db.query_nodes(_id=n4.id) == []


def test_jsonify_node(testdata):
    "A node can be serialized to python. The set of labels gets converted to a list"
    js = testdata.node.to_json(None)
    assert js == '''{"_id": "%s", "foo": "bar", "_labels": ["Testlabel"]}''' % testdata.node.id


def test_json_to_node(testdata):
    "Nodes can be updated from the respective json"
    n3 = Node(testdata.db)
    n3.from_json('''{"_id": "%s", "_labels": ["Testlabel"], "foo": "bar"}''' % testdata.node.id)
    assert n3 == testdata.node


def test_add_edge(db, testdata):
    "Adding an edge"
    edge1 = db.add_edge(testdata.alice, 'likes', testdata.bob, foo='bar')
    assert edge1 == dict(_id='...',
                         foo='bar')
    assert edge1.source == testdata.alice
    assert edge1.target == testdata.bob
    assert edge1.reltype == 'likes'
    assert edge1['foo'] == 'bar'


def test_update_edge(db, testdata):
    "Edges can be updated"
    testedge = db.add_edge(testdata.alice, 'test', testdata.bob, foo='bar')
    testedge['foo'] = 'bar2'
    edge2 = db.update_edge(testedge)
    assert edge2 == dict(_id='...',
                         foo='bar2')
    assert edge2.source == testdata.alice
    assert edge2.target == testdata.bob
    assert edge2.reltype == 'test'


def test_query_edge(db, testdata):
    testedge = db.add_edge(testdata.alice, 'testrel', testdata.bob, bar='foo')
    newedge = db.query_edges('testrel', bar='foo')[0]
    assert newedge == testedge
    newedge = db.query_edges(bar='foo')[0]
    assert newedge == testedge


def test_delete_edge(db, testdata):
    testedge = db.add_edge(testdata.alice, 'testrel', testdata.bob, bar='foo')
    assert len(db.query_edges(bar='foo')) > 0
    db.del_edge(testedge.id)
    assert len(db.query_edges(bar='foo')) == 0

def test_jsonify_edge(ld):
    "An edge can be serialized to python. The special properties are set"
    js = ld.e1.to_json(None)
    assert js == '''{"_id": "%s", "_source": "%s", "_target": "%s", "_reltype": "long"}''' % (
            ld.e1.id,
            ld.alice.id,
            ld.bob.id)

def test_json_to_edge(ld):
    js = '''{"_id": "%s", "_source": "%s", "_target": "%s", "_reltype": "long"}''' % (
            ld.e1.id,
            ld.alice.id,
            ld.bob.id)
    edge = Edge(ld.db)
    edge.from_json(js)
    assert edge == ld.e1



def test_edge_source_property(ld):
    e1 = ld.e1
    assert e1.source == ld.alice

def test_query_edge_source(db, ld):
    db = ld.db
    r = db.query_edges(source=ld.bob)
    assert r == [ld.e2]



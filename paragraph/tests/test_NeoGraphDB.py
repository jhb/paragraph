from paragraph.interfaces import Node

def test_create_node(db):
    "Create a node"

    n = db.add_node('Testlabel', foo='bar')
    assert n == {'_id': '...', '_labels': {'Testlabel'}, 'foo': 'bar'}


def test_update_node(db):
    "Update a node"

    n = db.add_node('Testlabel', foo='bar')

    n['foo2'] = 'bar2'
    n._labels.add('Testlabel2')

    n2 = db.update_node(n)
    assert n2 == {'_id':     '...',
                  '_labels': {'Testlabel2', 'Testlabel'},
                  'foo2':    'bar2',
                  'foo':     'bar'}


def test_jsonify_node(testdata):
    "A node can be serialized to python. The set of labels gets converted to a list"
    js = testdata.node.to_json(None)
    assert js == '''{"_id": "%s", "_labels": ["Testlabel"], "foo": "bar"}''' % testdata.node._id


def test_json_to_node(testdata):
    "Nodes can be updated from the respective json"
    n3 = Node()
    n3.from_json('''{"_id": "%s", "_labels": ["Testlabel"], "foo": "bar"}''' % testdata.node._id)
    assert n3 == testdata.node


def test_query_node(db, testdata):
    "Nodes can be queried"
    r = db.query_nodes(_id=testdata.node._id)
    assert r[0] == testdata.node


def test_delete_node(db):
    "Nodes can be deleted"

    # Lets add another node
    n4 = db.add_node('testnode')

    # Now its there
    r = db.query_nodes(_id=n4._id)
    assert r[0] == n4

    # Now its not...
    db.del_node(n4._id)
    assert db.query_nodes(_id=n4._id) == []


def test_add_edge(db, testdata):
    "Adding an edge"
    edge1 = db.add_edge(testdata.alice, 'likes', testdata.bob, foo='bar')
    assert edge1 == dict(_id='...',
                         _source=testdata.alice,
                         _reltype='likes',
                         _target=testdata.bob,
                         foo='bar')


def test_update_edge(db, testdata):
    "Edges can be updated"
    testedge = db.add_edge(testdata.alice, 'test', testdata.bob, foo='bar')
    testedge.foo = 'bar2'
    edge2 = db.update_edge(testedge)
    assert edge2 == dict(_id='...',
                         _source=testdata.alice,
                         _reltype='test',
                         _target=testdata.bob,
                         foo='bar2')


def test_query_edge(db, testdata):
    testedge = db.add_edge(testdata.alice, 'testrel', testdata.bob, bar='foo')
    newedge = db.query_edges('testrel', bar='foo')[0]
    assert newedge == testedge
    newedge = db.query_edges(bar='foo')[0]
    assert newedge == testedge


def test_delete_edge(db, testdata):
    testedge = db.add_edge(testdata.alice, 'testrel', testdata.bob, bar='foo')
    assert len(db.query_edges(bar='foo')) > 0
    db.del_edge(testedge._id)
    assert len(db.query_edges(bar='foo')) == 0


from paragraph.simpletraverser import SimpleTraverser


def test_simpletraverser_oN(linkeddata, db):
    ld = linkeddata
    t = SimpleTraverser(db, ld.alice)

    t2 = t.oN()
    assert ld.bob in t2.nodes
    assert ld.charlie in t2.nodes

    t2 = t.oN('long')
    assert ld.charlie not in t2.nodes

    t2 = t.oN('long', maxhops=2)
    assert ld.charlie in t2.nodes

    t2 = t.oN('long', maxhops=1)
    assert ld.bob in t2.nodes
    assert ld.charlie not in t2.nodes

    t2 = t.oN('short')
    assert ld.bob not in t2.nodes
    assert ld.charlie in t2.nodes


def test_simpletraverser_linked(linkeddata, db):
    ld = linkeddata
    t = SimpleTraverser(db, ld.alice)
    t2 = t.oN('long').oN('long')
    assert t2.nodes == [ld.charlie]

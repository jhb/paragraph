"""
Import and setup the database connector for Neo4j
    >>> from paragraph.NeoGraphDB import NeoGraphDB
    >>> db = NeoGraphDB(debug=1)

Create a node

    >>> n = db.add_node('Testlabel', foo='bar')
    >>> n == {'_id': '...', '_labels': {'Testlabel'}, 'foo': 'bar'}
    True

Upate the node
    >>> n['foo2']='bar2'
    >>> n._labels.add('Testlabel2')
    >>> n2 = db.update_node(n)
    >>> n2 == {'_id': '...',
    ...        '_labels': {'Testlabel2', 'Testlabel'},
    ...        'foo2': 'bar2',
    ...        'foo': 'bar'}
    True

It can be serialized to python. The set of labels gets converted to a list.
    >>> js = n.to_json()
    >>> print(js) # #doctest: +ELLIPSIS
    {
      "_id": "...",
      "_labels": [
        "Testlabel",
        "Testlabel2"
      ],
      "foo": "bar",
      "foo2": "bar2"
    }

And nodes can be updated from the respective json.
    >>> from paragraph.interfaces import Node
    >>> n3 = Node()
    >>> n3.from_json(js)
    >>> n3._similar_to(n,ellipsis='_no_elispis')
    True

Lets add another node
    >>> n4 = db.add_node('testnode')

Now its there
    >>> r = db.query_nodes(_id=n4._id)
    >>> r[0] == n4
    True

Now its not...
    >>> db.del_node(n4._id)
    >>> db.query_nodes(_id=n4._id)
    []

Three nodes to create edges
    >>> alice = db.add_node('Person',name='alice')
    >>> bob =  db.add_node('Person',name='bob')
    >>> charlie = db.add_node('Person',name='charlie')

add a simple edge
    >>> edge1 = db.add_edge(alice, 'likes', bob, foo='bar')
    >>> edge1 == dict(_source=alice, _target=bob,_reltype='likes',foo='bar',_id='...')
    True
"""

# paragraph
cms for labeled property graphs 

Usage example from neo4j:

    >>> from paragraph.NeoGraphDB import NeoGraphDB
    >>> db = NeoGraphDB()
    >>> alice = db.add_node('Person', name='alice')

Alice is a node. Nodes have a unique id and labels:

    >>> alice.id
    '...'
    >>> alice.labels
    {'Person'}

But a note also stores properties like a dictionary:

    >>> dict(alice)
    {'_id': '...', 'name': 'alice'}
    >>> alice.id == alice['_id']
    True

Why does id show up in the node properties, but not the labels? Because at least for neo4j labels
are stored on nodes anyhow, but id needs to be stored "manually", hence the property with the
special marker for technical attributes, the underscore "_".

Now lets link alice to bob:

    >>> bob = db.add_node('Person', name='bob')
    >>> edge = db.add_edge(alice, 'friend_of', bob, foo='bar')
    >>> edge.id
    '...'
    >>> edge.source == alice
    True
    >>> edge.target == bob
    True
    >>> edge.reltype
    'friend_of'


And again, all other properties are stored dictionary-style in the edge:

    >>> edge
    <Edge(NeoGraphDB(...),'...','friend_of','...')>
    >>> dict(edge)
    {'_id': '...', 'foo': 'bar'}

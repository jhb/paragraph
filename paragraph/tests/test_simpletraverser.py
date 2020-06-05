def test_simple_oN(ld):
    db = ld.db
    t_alice = db.traverse(name='alice')
    r = t_alice.oN('long')
    assert ld.bob in r.nodes


def test_oN(ld):
    db = ld.db

    r = db.traverse(name='alice').oN()
    assert ld.bob in r.nodes
    assert ld.charlie in r.nodes

    r = db.traverse(name='alice').oN('long')
    assert ld.charlie not in r.nodes

    r = db.traverse(name='alice').oN('long', maxhops=2)
    assert ld.bob in r.nodes
    assert ld.charlie in r.nodes

    r = db.traverse(name='alice').oN('long', maxhops=1)
    assert ld.bob in r.nodes
    assert ld.charlie not in r.nodes

    r = db.traverse(name='alice').oN('short')
    assert ld.bob not in r.nodes
    assert ld.charlie in r.nodes


def test_BN(ld):
    db = ld.db
    r = db.traverse(name='charlie').bN()
    assert r.nodes == {ld.alice,ld.bob,ld.dora}

def test_linked(ld):
    db = ld.db

    r = db.traverse(name='alice').oN('long').oN('long')
    assert r.nodes == {ld.charlie}


def test_minmax(ld):
    db = ld.db

    r = db.traverse(name='alice').oN(minhops=1, maxhops=3)
    assert r.nodes == {ld.bob, ld.charlie, ld.dora}

    r = db.traverse(name='alice').oN(minhops=2, maxhops=3)
    assert r.nodes == {ld.charlie, ld.dora}

    r = db.traverse(name='alice').oN(minhops=2, maxhops=2)
    assert r.nodes == {ld.charlie, ld.dora}

    r = db.traverse(name='alice').oN(minhops=3, maxhops=3)
    assert r.nodes == set()

    r = db.traverse(name='alice').oN('long',minhops=3, maxhops=3)
    assert r.nodes == {ld.dora}

    r = db.traverse(name='alice').oN('long', minhops=2, maxhops=2)
    assert r.nodes == {ld.charlie}

def test_nodes_seen(ld):
    db = ld.db

    r = db.traverse(name='alice').oN(minhops=2, maxhops=2)
    assert r.nodes == {ld.charlie,ld.dora}

    assert r.nodes_seen == {ld.alice,ld.bob,ld.charlie}

def test_backwards(ld):
    db = ld.db

    r = db.traverse(name='dora').iN(minhops=2,maxhops=2)
    assert r.nodes == {ld.alice,ld.bob}



def test_set(ld):
    s = set()
    s.add(ld.alice)
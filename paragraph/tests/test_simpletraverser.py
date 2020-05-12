
def test_simpletraverser_linked(linkeddata):
    ld = linkeddata
    db = ld.db

    r = db.traverse(name='alice').oN('long').oN('long')
    assert r.nodes == {ld.charlie}


def test_simpletraverser_minmax(linkeddata):
    ld = linkeddata
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

def test_simpletraverser_allnode(linkeddata):
    ld = linkeddata
    db = ld.db

    r = db.traverse(name='alice').oN(minhops=2, maxhops=2)
    assert r.nodes == {ld.charlie,ld.dora}

    print(r.nodes_seen)



def test_set(linkeddata):
    s = set()
    s.add(linkeddata.alice)
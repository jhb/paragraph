from paragraph import fields

def test_Field():

    f = fields.Field('23')
    assert int(f) == 23
    assert f.to_db() == '23'
    f.from_db('24')
    assert int(f) == 24


def test_StringField():

    f = fields.Field('foobar')
    assert str(f) == 'foobar'

def test_ListField():
    f = fields.ListField()
    assert f.value == []
    mylist = ['a','b','c']
    f2 = fields.ListField(mylist)
    serialized = f2.to_db()
    f3 = fields.ListField()
    f3.from_db(serialized)
    assert f3.value == mylist

def test_ListWidget():
    data = ['a','b','c']
    f = fields.ListField(data)
    lw = fields.ListWidget(f)
    assert lw.edit(name='bla') == '<textarea name="bla">a\nb\nc</textarea>'
    assert lw.html(name='bla') == '<ol name="bla"><li>a</li>\n<li>b</li>\n<li>c</li></ol>'

def test_HTMLWidget():
    data = '<h1>Testheading</h1>'
    f = fields.StringField(data)
    lh = fields.HTMlWidget(f)
    assert lh.edit(name='bla') == '<textarea name="bla"><h1>Testheading</h1></textarea>'
    assert lh.html(name='bla') == '<div name="bla"><h1>Testheading</h1></div>'
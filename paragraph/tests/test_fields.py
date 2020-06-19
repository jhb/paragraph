from paragraph import fields

def test_Field():

    f = fields.Field('23')
    assert int(f) == 23
    assert f.to_db() == '23'
    f.from_db('24')
    assert int(f) == 24

def test_Field_possible_widgets():
    f = fields.ListField()
    possible = f.possible_widgets()
    assert set(possible) == {fields.ListWidget,fields.LinesWidget}

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

def test_JsonOrStringField():
    data = ['a','b','c']
    f1 = fields.JsonOrStringField(data)
    serialized = f1.to_db()
    assert serialized == '[\n  "a",\n  "b",\n  "c"\n]'
    f2 = fields.JsonOrStringField()
    f2.from_db(serialized)
    assert f2.value == data
    f3 = fields.JsonOrStringField('foo')
    serialized = f3.to_db()
    assert serialized == 'foo'
    f4 = fields.JsonOrStringField()
    f4.from_db(serialized)
    assert f4.value == 'foo'

def test_YamlField():
    data = ['a','b','c']
    f1 = fields.YamlField(data)
    serialized = f1.to_db()
    assert serialized == '- a\n- b\n- c\n'
    f2 = fields.YamlField()
    f2.from_db(serialized)
    assert f2.value == data
    f3 = fields.YamlField('foo')
    serialized = f3.to_db()
    assert serialized == 'foo\n...\n'
    f4 = fields.YamlField()
    f4.from_db(serialized)
    assert f4.value == 'foo'

def test_ScriptField(ld):
    script = "result='hello '+ 'world'"
    f = fields.ScriptField(script)
    assert f.value == script
    assert str(f) == 'hello world'
    script2 = 'print(foobar)'
    f2 = fields.ScriptField(script2)
    assert "== Error on input line 1 ==" in str(f2)
    script3 = "result=db.query_nodes(name='alice')"
    f3 = fields.ScriptField(script3,db=ld.db)
    result = f3.get_value()
    assert result.nodes[0] == ld.alice

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

def test_combos():
    print(fields.all_combos())

def test_jhb():
    f = fields.JsonOrStringField(['a','b','c',['x%s'  % i  for i in range(5)],dict(foo=1,bar=2)])
    w = fields.TextWidget(f)
    print(w.edit())
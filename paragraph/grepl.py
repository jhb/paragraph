import pprint

import IPython
from paragraph.NeoGraphDB import NeoGraphDB
from paragraph.basic import ObjectDict

def populate(db):
    data = ObjectDict()
    data.db = db
    data.node = data.db.add_node('Testlabel', foo='bar')
    data.alice = data.db.add_node('Person', name='alice')
    data.bob = data.db.add_node('Person', name='bob')
    data.charlie = data.db.add_node('Person', name='charlie')
    data.dora = data.db.add_node('Person', name='dora')
    data.e1 = db.add_edge(data.alice, 'long', data.bob)
    data.e2 = db.add_edge(data.bob, 'long', data.charlie)
    data.e4 = db.add_edge(data.alice, 'short', data.charlie)
    data.e3 = db.add_edge(data.charlie, 'long', data.dora)
    return data

db = NeoGraphDB()
if len(db.query_nodes()) == 0:
    data = populate(db)
    db.commit()
scope_vars = dict(db=db,data=data)

header = "Welcome to the Grepl! You have the following objects today:\n\r"
header+'\n\r'
header+=pprint.pformat(scope_vars)
footer = "Thanks a lot!"

try:
    raise ImportError()
    import IPython
except ImportError:
    from code import InteractiveConsole
    InteractiveConsole(locals=scope_vars).interact(header, footer)
else:
    print(header)
    IPython.start_ipython(argv=[], user_ns=scope_vars)
    print(footer)


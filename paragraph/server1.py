import abc
from collections import UserList, OrderedDict

from flask import Flask, request
from paragraph.NeoGraphDB import NeoGraphDB
from paragraph.simpletraverser import SimpleTraverser
import sys
from io import StringIO
from paragraph.basic import ObjectDict
import neo4j
from paragraph.tal_templates import TalTemplates

app = Flask(__name__)

templates = TalTemplates()
db = NeoGraphDB()

@app.route('/')
def hello_world():
    return templates.index(foo=0)

class ResultWrapper:

    def __init__(self,data):
        if type(data) in [neo4j.BoltStatementResult]:
            result = data
            data = UserList()
            for row in result:
                rowdict = OrderedDict()
                for key in row.keys():
                    value = row[key]
                    if type(value) == neo4j.Node:
                        value = db._neo2node(value)
                    elif type(value) in [neo4j.Relationship] or hasattr(value,'start_node'): # neo4j, I love you
                        value = db._neo2edge(value)
                    rowdict[key]=value
                data.append(rowdict)
            graph = result.graph()
            data.nodes = []
            data.edges = []
            for n in graph.nodes:
                data.nodes.append(db._neo2node(n))
            for r in graph.relationships:
                data.edges.append(db._neo2edge(r))
        elif type(data) in [SimpleTraverser]:
            pass
        else:
            data = dict(data=data)
        self.data=data


    def _getattribute(self,key,default):
        if hasattr(self.data,key):
            return getattr(self.data,key,default)
        elif hasattr(self.data,key):
            return self.data.get(key,default)
        else:
            return default

    @property
    def nodes(self):
        return self._getattribute('nodes',[])

    @property
    def edges(self):
        return self._getattribute('edges',[])

    def items(self):
        if hasattr(self.data,'items'):
            return self.data.items()
        else:
            return tuple()

@app.route('/query')
def query():
    result = ObjectDict()
    if request.values:
        print(request.values.get('statement'))
        printed = StringIO()
        vars = ObjectDict(printed=printed, db=db,result=None)
        stdout = sys.stdout
        try:
            sys.stdout = printed
            exec(request.values.get('statement', ''), vars)
            result = vars.get('result', None)
            sys.stdout = stdout
            printvalue = printed.getvalue()
        except Exception as e:
            printvalue = printed.getvalue()
            sys.stdout=stdout
        finally:
            sys.stdout=stdout
    else:
        printvalue = ''
    return templates.query(db=db,result=ResultWrapper(result),ObjectDict=ObjectDict,printvalue=printvalue)


if __name__ == '__main__':
    app.run(debug=True)

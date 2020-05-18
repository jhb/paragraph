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
            data = ObjectDict()
            for r in result:
                for key in r.keys():
                    data.setdefault(key,[]).append(r[key])
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


def magichands(self):
    context = self.context
    self.lastoutput = ''
    self.lastcode = ''
    self.haserror = 0

    printed = StringIO()
    if self.request.method.lower() == 'post':
        code = self.request.code
        vars = globals()
        stdout = sys.stdout
        vars['printed'] = printed
        vars['context'] = context
        vars['request'] = context.REQUEST
        vars['response'] = context.REQUEST.RESPONSE
        vars['sysout'] = stdout
        # newcode = "import sys; sys.stdout=printed\n\n" + code.replace('\r','')
        newcode = code.replace('\r', '')
        try:
            sys.stdout = printed
            exec(newcode, vars)
            self.lastoutput = vars.get('output', vars['printed'].getvalue())
            sys.stdout = stdout
        except Exception as e:
            self.haserror = 1
            sys.stdout = stdout
            exinfo = sys.exc_info()
            top = exinfo[2]
            line = '?? - see below'
            if top.tb_next:
                top = exinfo[2].tb_next
                line = top.tb_lineno
            self.lastoutput = vars['printed'].getvalue()
            self.lastoutput += """\n== Error on input line %s ==\n%s: %s\n""" % (line, e.__class__.__name__, str(e))
        finally:
            sys.stdout = stdout
        self.lastcode = code
    return ViewPageTemplateFile('magichands.pt')(self)


if __name__ == '__main__':
    app.run(debug=True)

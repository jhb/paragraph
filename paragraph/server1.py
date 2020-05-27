import abc
from collections import UserList, OrderedDict, UserDict
import mimetypes
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('text/javascript', '.js')


from flask import Flask, request
from paragraph.NeoGraphDB import NeoGraphDB
from paragraph.simpletraverser import SimpleTraverser
import sys
from io import StringIO
from paragraph.basic import ObjectDict, ResultWrapper
import neo4j
from paragraph.tal_templates import TalTemplates

app = Flask(__name__)

templates = TalTemplates()
db = NeoGraphDB()

@app.route('/')
def hello_world():
    return templates.index(foo=0)



@app.route('/query')
def query():
    result =None
    if request.values:
        print(request.values.get('statement'))
        printed = StringIO()
        vars = ObjectDict(printed=printed, db=db,result=None, SimpleTraverser=SimpleTraverser)
        stdout = sys.stdout
        try:
            sys.stdout = printed
            exec(request.values.get('statement', ''), vars)
            result = vars.get('result', None)
            sys.stdout = stdout
            printvalue = printed.getvalue()
            db.rollback()
        except Exception as e:
            sys.stdout=stdout
            exinfo = sys.exc_info()
            top = exinfo[2]
            line = '?? - see below'
            if top.tb_next:
                top = exinfo[2].tb_next
                line = top.tb_lineno
            printvalue = printed.getvalue()
            printvalue += """\n== Error on input line %s ==\n%s: %s\n""" %(line, e.__class__.__name__,str(e))
        finally:
            sys.stdout=stdout
    else:
        printvalue = ''
    if not isinstance(result, ResultWrapper):
        result = ResultWrapper(result)
    return templates.query(db=db,result=result, printvalue=printvalue)

@app.route('/show_node/<string:node_id>')
def show_node(node_id):
    result = db.query_nodes(_id=node_id)
    return templates.show_node(db=db,node=result[0])

@app.route('/edit_node/<string:node_id>')
def edit_node(node_id):
    result = db.query_nodes(_id=node_id)
    return templates.edit_node(db=db,node=result[0])


@app.route('/show_edge/<string:edge_id>')
def show_edge(edge_id):
    result = db.query_edges(_id=edge_id)
    return templates.show_edge(db=db,edge=result[0])



if __name__ == '__main__':
    app.run(debug=True)

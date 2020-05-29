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
from flask_wtf import FlaskForm
from wtforms import Form,StringField

app = Flask(__name__)

templates = TalTemplates()
db = NeoGraphDB(debug=0)

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

@app.route('/edit_node/<string:node_id>', methods=['GET','POST'])
def edit_node(node_id):
    node = db.query_nodes(_id=node_id)[0]
    if request.form:
        class MyForm(Form):
            labels = StringField('labels')
        for k,v in node.items():
            if k in ['_id']:
                continue
            vt = type(v)
            if vt is str or 1:
                setattr(MyForm,k,StringField(k))
        for k in ['name','value','type']:
            name = 'newprop_'+k
            setattr(MyForm,name,StringField(name))
        form = MyForm(request.form)
        if form.validate():
            keys = list(node.keys())
            for k in keys:
                if '_delete_'+k in request.form:
                    del(node[k])
            for k in node.keys():
                if k in ['_id']:
                    continue

                node[k]=form[k].data
            node.labels = set([l.strip() for l in form.labels.data.split(',')])
            if form.newprop_name.data and form.newprop_value.data and form.newprop_type.data:
                typemap = dict(string=str,integer=int, int=int)
                newtype = typemap.get(form.newprop_type.data,str)
                value = newtype(form.newprop_value.data)
                name = form.newprop_name.data
                if name not in ['_id']:
                    node[name]=value
            node = db.update_node(node)
            db.commit()


    return templates.edit_node(db=db,node=node)


@app.route('/show_edge/<string:edge_id>')
def show_edge(edge_id):
    result = db.query_edges(_id=edge_id)
    return templates.show_edge(db=db,edge=result[0])



if __name__ == '__main__':
    app.run(debug=True)

import abc
import os
from collections import UserList, OrderedDict, UserDict
import mimetypes

from paragraph import fields

mimetypes.add_type('text/css', '.css')
mimetypes.add_type('text/javascript', '.js')

import traceback
from flask import Flask, request, send_from_directory
from paragraph.NeoGraphDB import NeoGraphDB
from paragraph.simpletraverser import SimpleTraverser
import sys
from io import StringIO
from paragraph.basic import ObjectDict, ResultWrapper
import neo4j
from paragraph.tal_templates import TalTemplates
from flask_wtf import FlaskForm
import wtforms as wtf
from wtforms import Form,StringField
from paragraph.execute import run_script
from paragraph import fields
from dotenv import find_dotenv, load_dotenv

load_dotenv()

files = os.path.join(os.path.dirname(find_dotenv()), os.getenv("FILEPATH"))
os.environ['FILES']=files

app = Flask(__name__)
# turn of caching for static files during development
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

templates = TalTemplates()
db = NeoGraphDB(debug=0)

typemap = dict(string=str,integer=int, boolean='bool')


@app.route('/')
def hello_world():
    return templates.index(foo=0)



@app.route('/gmi')
def gmi():
    result =None
    if request.values:
        statement = request.values.get('statement', '')
        print(statement)
        result, printvalue = run_script(statement, db=db, result=None, SimpleTraverser=SimpleTraverser)
    else:
        printvalue = ''

    if not isinstance(result, ResultWrapper):
        result = ResultWrapper(result)

    return templates.gmi(db=db,result=result, printvalue=printvalue)

@app.route('/show_node/<string:node_id>')
def show_node(node_id):
    result = db.query_nodes(_id=node_id).nodes
    return templates.show_node(db=db,node=result[0])


def edit_obj(obj,request,excluded=['_id']):
    propdict = db.propdict

    _field_class = getattr(fields,propdict['_field']['_field'])

    def getPropFieldClass(name,default=fields.StringField): # 00_todo what should be the default? @@_todo
        if name in propdict:
            prop = propdict[name]
            fname = _field_class(prop['_field']).get_value()
            fieldclass = getattr(fields, fname, default)
        else:
            fieldclass = default
        return fieldclass

    class MyForm(wtf.Form):
            labels = wtf.StringField('labels')

    for k,v in obj.items():
        if k in ['_id']:
            continue
        vt = type(v)
        if vt is str or 1:
            setattr(MyForm,'formdata_'+k,wtf.StringField('formdata_'+k))
    for k in ['name','value','type']:
        name = 'newprop_'+k
        setattr(MyForm,name,wtf.StringField(name))

    MyForm.applyschema=wtf.StringField('applyschema') # 00_todo replace by proper string field

    form = MyForm(request.form)
    if form.validate():
        keys = list(obj.keys())
        for k in keys:
            if '_delete_'+k in request.form:
                del(obj[k])
        for k in obj.keys():
            if k in excluded:
                continue

            #obj[k]=form['formdata_'+k].data
            fieldclass = getPropFieldClass(k)
            value = fieldclass(form['formdata_'+k].data).value
            obj[k]=value
        obj.labels = set([l.strip() for l in form.labels.data.split(':') if l])

        if form.newprop_name.data and form.newprop_type.data:
            name = form.newprop_name.data
            # hack for lazy property form in node_edit
            if ' - ' in name:
                name = name.split(' - ')[0].strip()


            # get type from property, otherwise from typemap
            if name in propdict:
                fieldclass = getPropFieldClass(name)
                f = fieldclass(form.newprop_value.data)
                value = f.value # 00_todo f.get_value, but ScriptFields
                print('Field',f.__class__)
            else:
                newtype = typemap.get(form.newprop_type.data,str)
                value = newtype(form.newprop_value.data) or ''

            if name not in excluded:
                obj[name]=value

        if form.applyschema.data:
            db.schemahandler.apply_to_node(form.applyschema.data,obj)

        return True
    else:
        return False



def getWidget(obj, propname, defaultfield=fields.StringField, defaultwidget=fields.StringWidget):
    value = obj[propname]
    if propname in db.propdict:
        prop = db.propdict[propname]
        fieldclassname = prop.get('_field','')
        fieldclass = getattr(fields, fieldclassname, defaultfield)
        field = fieldclass(value,obj=obj, db=db, prop=prop)
        widgetclassname = prop.get('_widget','')
        widgetclass = getattr(fields, widgetclassname, defaultwidget)
        widget = widgetclass(field)
        return widget
    else:
        return defaultwidget(defaultfield(value))




@app.route('/edit_node/<string:node_id>', methods=['GET','POST'])
def edit_node(node_id):
    node = db.query_nodes(_id=node_id).nodes[0]
    if request.form:
        validated = edit_obj(node,request)
        if validated:
            node = db.update_node(node)
            db.commit()
    return templates.edit_node(db=db,node=node,typemap=typemap, getWidget=getWidget)

@app.route('/edit_edge/<string:edge_id>', methods=['GET','POST'])
def edit_edge(edge_id):
    edge = db.query_edges(_id=edge_id).edges[0]
    if request.form:
        validated = edit_obj(edge,request)
        if validated:
            edge = db.update_edge(edge)
            db.commit()
    return templates.edit_edge(db=db,edge=edge,typemap=typemap, getWidget=getWidget)

@app.route('/add_node')
def add_node():
    node = db.add_node()
    db.commit()
    return node.id

@app.route('/delete_node/<string:node_id>')
def delete_node(node_id):
    db.del_node(node_id,True)
    db.commit()
    return ''

@app.route('/show_edge/<string:edge_id>')
def show_edge(edge_id):
    result = db.query_edges(_id=edge_id)
    return templates.show_edge(db=db,edge=result[0])

@app.route('/add_edge', methods=['GET','POST'])
def add_edge():
    if request.form:
        edge = db.add_edge(request.form['source'],
                           request.form['reltype'],
                           request.form['target'])
        db.commit()
        return templates.edit_edge(db=db,edge=edge)
    else:
        return templates.add_edge(db=db)


@app.route('/delete_edge/<string:edge_id>')
def delete_edge(edge_id):
    db.del_edge(edge_id)
    db.commit()
    return ''

@app.route('/files/<path:path>')
def files(path):
    return send_from_directory(os.getenv('FILES'),path)


if __name__ == '__main__':

    app.run('0.0.0.0', debug=True, )


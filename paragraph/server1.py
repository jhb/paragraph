import abc
from collections import UserList, OrderedDict, UserDict

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
    if not isinstance(result, ResultWrapper):
        result = ResultWrapper(result)
    return templates.query(db=db,result=result, printvalue=printvalue)


if __name__ == '__main__':
    app.run(debug=True)

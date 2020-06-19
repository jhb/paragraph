import sys
from io import StringIO
from flask import request
import traceback


def run_script(code,vars=None):
    if vars is None:
        vars = {}
    printed = StringIO()
    vars['printed'] = printed
    stdout = sys.stdout
    request.stdout = stdout
    result = None
    try:
        sys.stdout = printed
        exec(code, vars)
        result = vars.get('result', None)
        sys.stdout = stdout
        printvalue = printed.getvalue()
    except Exception as e:
        sys.stdout = stdout
        exinfo = sys.exc_info()
        top = exinfo[2]
        line = '?? - see below'
        if top.tb_next:
            top = exinfo[2].tb_next
            line = top.tb_lineno
        printvalue = printed.getvalue()
        printvalue += """\n== Error on input line %s ==\n%s: %s\n \n%s""" % (line,
                                                                             e.__class__.__name__,
                                                                             str(e),
                                                                             traceback.format_exc())
    finally:
        sys.stdout = stdout
    return result, printvalue
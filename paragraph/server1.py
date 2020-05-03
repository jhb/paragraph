from flask import Flask

from paragraph.tal_templates import TalTemplates

app = Flask(__name__)

templates = TalTemplates()


@app.route('/')
def hello_world():
    return templates.index(foo=0)


if __name__ == '__main__':
    app.run(debug=True)

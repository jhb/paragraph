import sys
import inspect
import json
import io

import yaml

from paragraph.execute import run_script


class Field:

    dbtype = 'string'

    def _default(self):
        return ''

    def possible_widgets(self):
        clsmembers = [i[1] for i in inspect.getmembers(sys.modules[__name__], inspect.isclass)]
        myclass = self.__class__
        return [cls for cls in clsmembers if myclass in getattr(cls,'possible_fields',[])]

    def __init__(self, value=None, **kwargs):
        if value is None:
            value = self._default()
        self.value = value
        self.kwargs=kwargs

    def get_value(self):
        return self.value

    def __str__(self):
        return str(self.get_value())

    def __int__(self):
        return int(self.get_value())

    def __float__(self):
        return float(self.get_value())

    def to_db(self):
        return str(self)

    def from_db(self, value):
        self.value = value
        return self.value


class StringField(Field):
    pass

class ListField(Field):

    def _default(self):
        return []

    def to_db(self):
        return '|||'.join([str(v) for v in self.value])

    def from_db(self,value):
        self.value = value.split('|||')
        return self.value

class JsonOrStringField(Field):

    def __str__(self):
        return self.to_db()

    def to_db(self):
        if type(self.value) == str:
            return self.value
        else:
            out = json.dumps(self.value, indent=2)
            #print(out)
            return out

    def from_db(self, value):
        try:
            v = json.loads(value)
        except json.decoder.JSONDecodeError as e:
            v = value
        self.value = v
        return self.value

class YamlField(Field):

    def __str__(self):
        return self.to_db()

    def to_db(self):
        return yaml.safe_dump(self.value)

    def from_db(self, value):
        self.value = yaml.safe_load(value)
        return self.value

class ScriptField(Field):

    def get_value(self):
        result, printvalue = run_script(self.value,**self.kwargs)
        if result:
            return result
        else:
            return printvalue


class CSVLineField(Field):

    def __str__(self):
        return self.to_db()

    def to_db(self):
        return ';'.join(self.value)

    def from_db(self,value):
        self.value = [v.strip() for v in value.split(';')]
        return self.value

class Widget:

    possible_fields = [StringField]
    uik = "uk-input"

    def __init__(self,field):
        self.field = field

    def _kw2attr(self,**kwargs):
        if 'klass' in kwargs:
            kwargs['class']=kwargs['klass']
            del(kwargs['klass'])

        return ' '.join([f'{k}="{v}"' for k,v in kwargs.items()])

    def edit(self,**kwargs):
        kwargs['value']=str(self.field)
        return f'<input {self._kw2attr(**kwargs)}/>'

    def view(self, _tag='span', **kwargs):
        return self.html(_tag, **kwargs)

    def html(self, _tag='span', **kwargs):
        return f"<{_tag} {self._kw2attr(**kwargs)}>{str(self.field.value)}</{_tag}>"

class StringWidget(Widget):
    possible_fields = [StringField, CSVLineField]

class LinesWidget(Widget):
    uik = "uk-textarea"

    possible_fields = [ListField]

    def edit(self,**kwargs):
        return "<textarea %s>%s</textarea>" % (self._kw2attr(**kwargs),
                                               "\n".join([str(v) for v in self.field.value]))
    def html(self,  _tag='span',**kwargs):
        return "<{_tag} {self._kw2attr(**kwargs)}> {'<br>'.join(self.field.value)}<{/_tag}>"

class ListWidget(LinesWidget):

    possible_fields = [ListField]

    def html(self,  _tag='ol',**kwargs):
        data = '\n'.join([f'<li>{v}</li>' for v in self.field.value])
        return f"<{_tag} {self._kw2attr(**kwargs)}>{data}</{_tag}>"


class TextAreaWidget(Widget):
    uik = "uk-textarea"

    possible_fields = [StringField, JsonOrStringField, YamlField, ScriptField]

    def edit(self,**kwargs):
        return "<textarea %s>%s</textarea>" % (self._kw2attr(**kwargs),
                                               str(self.field))

class HTMlWidget(TextAreaWidget):
    possible_fields = [StringField]

    # #use some wysiwyg editor for edit, or md

    def html(self, _tag='div', **kwargs):
        return super().html(_tag,**kwargs)


def all_combos():
    combos = []
    clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for name, widget in clsmembers:
        if not issubclass(widget,Widget) or widget == Widget:
            continue
        wname = widget.__name__
        for field in widget.possible_fields:
            fname = field.__name__
            name = f' {fname} with {wname}'
            combos.append(name)
    return sorted(combos)

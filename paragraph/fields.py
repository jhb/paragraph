class Field:

    dbtype = 'string'

    def _default(self):
        return ''

    def __init__(self, value=None):
        if value is None:
            value = self._default()
        self.value = value

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

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



class Widget:

    def __init__(self,field):
        self.field = field

    def _kw2attr(self,**kwargs):
        return ' '.join([f'{k}="{v}"' for k,v in kwargs.items()])

    def edit(self,**kwargs):
        kwargs['value']=str(self.field)
        return f'<input {self._kw2attr(**kwargs)}/>'

    def html(self, _tag='span', **kwargs):
        return f"<{_tag} {self._kw2attr(**kwargs)}>{self.field.value}</{_tag}>"

class LinesWidget(Widget):

    def edit(self,**kwargs):
        return "<textarea %s>%s</textarea>" % (self._kw2attr(**kwargs),
                                               "\n".join([str(v) for v in self.field.value]))
    def html(self,  _tag='span',**kwargs):
        return "<{_tag} {self._kw2attr(**kwargs)}> {'<br>'.join(self.field.value)}<{/_tag}>"

class ListWidget(LinesWidget):

    def html(self,  _tag='ol',**kwargs):
        data = '\n'.join([f'<li>{v}</li>' for v in self.field.value])
        return f"<{_tag} {self._kw2attr(**kwargs)}>{data}</{_tag}>"

class HTMlWidget(Widget):

    def edit(self,**kwargs): #use some wysiwyg editor for this, or md
        return "<textarea %s>%s</textarea>" % (self._kw2attr(**kwargs),
                                               self.field.value)

    def html(self, _tag='div', **kwargs):
        return super().html(_tag,**kwargs)



from chameleon import PageTemplate, PageTemplateLoader
import os
import flask

class TalTemplateWrapper:

    def __init__(self,template,**kwargs):
        self.template=template
        self.kwargs=kwargs

    def __call__(self, **kwargs):
        kwargs.update(self.kwargs)
        return self.template(**kwargs)

class TalTemplates:

    def __init__(self,templatedir=None, suffix='.pt'):
        self.suffix = suffix
        if templatedir is None:
            templatedir = os.path.join(os.path.dirname(__file__), 'templates')
        self.templatedir = templatedir

    def _loader(self):
        return PageTemplateLoader(self.templatedir,self.suffix)

    def __getitem__(self, item):
        templates = self._loader()
        req = flask.request
        if req.values.get('_ajax'):
            ajaxcontent = templates[item].macros['ajax']
            return TalTemplateWrapper(templates['ajax'], ajaxcontent=ajaxcontent, flask=flask, templates=templates)
        else:
            return TalTemplateWrapper(templates[item],flask=flask,templates=templates)

    def __getattr__(self, item):
        return self[item]



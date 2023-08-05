
from .util import Tag
from melan import Format
from collections import defaultdict

# ------------------------------------------------------------------------

class Document:
    __slots__ = ('_lang','_enc','_data','_base','_title')
    def __init__(self,lang='en',enc='utf-8'):
        self._lang = lang
        self._enc = enc
        self._data = defaultdict(list)

        # force these two to strings
        self._base = None
        self._title = None
    
    # ----------  =====  ----------
    
    def wrap(self,fun):
        self._data['wrap'].append(fun)
        return self

    def lang(self,lang):
        self._lang = lang
        return self

    def enc(self,enc):
        self._enc = enc 
        return self

    def base(self,**kv):
        self._base = Tag('base',**kv)
        return self

    def title(self,t):
        self._title = Tag('title').body(t)
        return self

    def meta(self,**kv):
        self._data['meta'].append(Tag('meta',**kv))
        return self
    
    def style(self,body,**kv):
        self._data['style'].append(Tag('style',**kv).body(body))
        return self

    def link(self,**kv):
        self._data['link'].append(Tag('link',**kv))
        return self

    def tscript(self,body,**kv):
        self._data['tscript'].append(Tag('script',**kv).body(body))
        return self

    def bscript(self,body,**kv):
        self._data['bscript'].append(Tag('script',**kv).body(body))
        return self
    
    # ----------  =====  ----------
    
    def str(self,body=None):

        # put header together
        head = Tag('head')
        head.append(Tag('meta',charset=self._enc))
        head.extend(self._data['meta'])
        head.append(self._base)
        head.append(self._title)
        head.extend(
            self._data['link'] + 
            self._data['tscript'] + 
            self._data['style']
        )

        # wrap body and append scripts
        for fun in self._data['wrap']:
            body = fun(body)

        body = Tag('body').body(body)
        body.extend(self._data['bscript'])

        # force head and body to span multiple lines
        head.inline(False)
        body.inline(False)

        # assemble
        doc = Tag('html',lang=self._lang).append(head).append(body)
        return '<!doctype html>\n' + doc.str()

# ------------------------------------------------------------------------

class Format_HTML(Format):
    def __init__(self):
        super().__init__('html')
        self.doc = Document()

    def __call__(self,cpl,body):
        return self.doc.str(body)

    def wrap(self,fun):
        self.doc.wrap(fun)
        return self
    
    # ----------  =====  ----------
    
    def lang(self,cpl,lang):
        self.doc.lang(lang)
        return self

    def base(self,cpl,_,**kv):
        self.doc.base(**kv)
        return self

    def title(self,cpl,title):
        self.doc.title(title)
        return self

    def meta(self,cpl,_,**kv):
        self.doc.meta(**kv)
        return self
    
    def style(self,cpl,body,**kv):
        self.doc.style(body,**kv)
        return self

    def link(self,cpl,_,**kv):
        self.doc.link(**kv)
        return self

    def tscript(self,cpl,body,**kv):
        self.doc.tscript(body,**kv)
        return self

    def bscript(self,cpl,body,**kv):
        self.doc.bscript(body,**kv)
        return self
    
    # ----------  =====  ----------

    def setup(self,cpl,_,lang='en',charset='utf-8'):
        self.doc.lang(lang).enc(charset)
        return self
    
    def css(self,cpl,body,**kv):
        self.doc.link( rel='stylesheet', href=body, **kv )
        return self

    def jstlib(self,cpl,body,**kv):
        self.doc.tscript( '', type='text/javascript', src=body, **kv )
        return self

    def jsblib(self,cpl,body,**kv):
        self.doc.bscript( '', type='text/javascript', src=body, **kv )
        return self

    def jscode(self,cpl,body,**kv):
        self.doc.bscript( body, type='text/javascript', **kv )
        return self

    def plugin(self,cpl,name,prefix='',ext=False,**kv):
        if not ext: name = f'html.plugin.{name}'
        x = cpl.import_export( name )
        x.pop('cfg')(cpl,self,**kv)
        cpl.load_dict( x, prefix=prefix )
        return self

# ------------------------------------------------------------------------

obj = Format_HTML()

export = {
    'pre': {
        'lang': obj.lang, 'base': obj.base, 'title': obj.title,
        'meta': obj.meta, 'style': obj.style, 'link': obj.link,
        'tscript': obj.tscript, 'bscript': obj.bscript, 'css': obj.css,
        'jstlib': obj.jstlib, 'jsblib': obj.jsblib, 'jscode': obj.jscode,
        'setup': obj.setup, 'plugin': obj.plugin
    },
    'fmt': obj
}

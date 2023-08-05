
from .util import *

import re
import html
from urllib.parse import quote_plus as urlenc

# ------------------------------------------------------------------------

_stack = None

def init(cpl):
    global _stack
    _stack = cpl.stack
    _stack.restrict('list',['item'])
    _stack.restrict('details',['summary','par'])
    _stack.restrict('table',['head','body','caption'])
    _stack.restrict('head',['row'])
    _stack.restrict('body',['row'])
    _stack.restrict('row',['col','title'])

# ------------------------------------------------------------------------

def h1(body,**kv): return qtag('h1',body,**kv)
def h2(body,**kv): return qtag('h2',body,**kv)
def h3(body,**kv): return qtag('h3',body,**kv)
def h4(body,**kv): return qtag('h4',body,**kv)
def h5(body,**kv): return qtag('h4',body,**kv)
def h6(body,**kv): return qtag('h5',body,**kv)
def par(body,**kv): return qtag('p',body,**kv)

def nl(body): return qtag('br')
def kbd(body): return qtag('kbd',body)
def abbr(body): return qtag('abbr',body)
def small(body): return qtag('small',body)

def inserted(body): return qtag('ins',body)
def deleted(body): return qtag('del',body)

def c(body,**kv): return qtag('code',html.escape(body),**kv)
def hl(body,**kv): return qtag('mark',body)
def hr(_,width=2,**kv): 
    return qtag('hr',None,**kv).addStyle(f'border-width:{width}px')
    
def b(body): return qtag('b',body)
def i(body): return qtag('i',body)
def u(body): return qtag('u',body)
def s(body): return qtag('s',body)
def em(body): return qtag('em',body)
def im(body): return qtag('strong',body)

# ------------------------------------------------------------------------

def url(href,text=None,ext=False,**kv): 
    if text is None: text = href 
    if ext: kv['target'] = '_blank'
    kv['href'] = unquote(href)
    return qtag('a',text,**kv)

def email(body,text=None,subject=None,**kv):
    if text is None: text = body 
    if subject is None:
        kv['href'] = f'mailto:{body}'
    else:
        kv['href'] = f'mailto:{body}?subject={urlenc(subject)}'
    return qtag('a',text,**kv)

def image(body,**kv): 
    kv['src'] = unquote(body)
    return qtag('img',None,**kv)

def code(body,lang=None,**kv):
    p = Tag('pre',data_lang=lang)
    c = Tag('code',**kv).body(html.escape(body))
    if lang:
        p.addClass(f'language-{lang}')
        c.addClass(f'language-{lang} lang-{lang}')
    return p.append(c).str()

def quote(body,**kv):
    return qtag('blockquote',body,**kv)

def itemize(body,enum=False,**kv):
    name = 'ol' if enum else 'ul'
    return qtag(name,body,**kv)

def describe(body,**kv):
    return qtag('dl',body,**kv)

def item(body,**kv):
    if _stack.parent == 'list':
        return qtag('li',body,**kv)
    elif _stack.parent == 'describe':
        return qtag('dl',body,**kv)
    else:
        raise NameError(f'Bad item scope: {_stack.parent}')

def address(body,**kv):
    return qtag('address',body,**kv)

def details(body,**kv):
    return qtag('details',body,**kv)

def summary(body):
    return qtag('summary',body)

# ------------------------------------------------------------------------

def table(body,**kv):
    return qtag('table',body,**kv)

def table_head(body,**kv):
    return qtag('thead',body,**kv)

def table_body(body,**kv):
    return qtag('tbody',body,**kv)

def table_title(body,**kv):
    out = qtag('th',body,**kv)
    if _stack[-3] == 'head':
        out['scope'] = 'col'
    elif _stack[-3] == 'body':
        out['scope'] = 'row'
    else:
        raise NameError(f'Bad title scope: {_stack.parent}')
    return out

def table_row(body,**kv):
    return qtag('tr',body,**kv)

def table_col(body,head=False,span=None,**kv):
    name = 'th' if head else 'td'
    if span: kv['colspan'] = f'{span}'
    return qtag(name,body,**kv)

# ------------------------------------------------------------------------

export = {
    'ini': init,
    'doc': {
        'h1': h1, 'h2': h2, 'h3': h3, 'h4': h4, 'h5': h5, 'h6': h6, 'par': par, 
        'c': c, 'b': b, 'i': i, 'u': u, 's': s, 'em': em, 'im': im, 
        'nl': nl, 'kbd': kbd, 'abbr': abbr, 'small': small, 'hr': hr, 'hl': hl,
        'ins': inserted, 'del': deleted, 'url': url, 'email': email, 
        'image': image, 'code': code, 'quote': quote, 
        'list': itemize, 'describe': describe, 'item': item,
        'address': address, 'details': details, 'summary': summary,
        'table': table, 'head': table_head, 'body': table_body, 
        'title': table_title, 'row': table_row, 'col': table_col
    }
}

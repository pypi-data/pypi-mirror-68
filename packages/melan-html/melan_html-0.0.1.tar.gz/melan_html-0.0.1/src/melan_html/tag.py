
from melan.util import dedent

# ------------------------------------------------------------------------

def attr2str(attr):
    out = []
    for k,v in attr.items():
        if k == 'className':
            k = 'class'
        else:
            k = k.replace('_','-')
        if isinstance(v,bool):
            out.append(f' {k}' if v else '')
        else:
            out.append(f' {k}="{v}"')
    return ''.join(out)

# ------------------------------------------------------------------------

class QuickTag:
    __slots__ = ('_name','_attr','_body')
    def __init__(self,name,**attr):
        self._name = name 
        self._attr = dict(attr)
        self._body = None

    def __str__(self):
        name = self._name
        attr = attr2str(self._attr)

        if self._body is None:
            return f'<{name}{attr} />'
        else:
            return f'<{name}{attr}>{self._body}</{name}>'

        # return f'<{name}{attr}>\n{self._body}</{name}>'
        
    # body
    def body(self,val):
        if isinstance(val,str) or val is None:
            self._body = val
        else:
            raise TypeError(f'Unexpected body type: {type(val)}')
        return self

    # attributes
    def __getitem__(self,prop):
        return self._attr[prop]
    def __setitem__(self,prop,val):
        self._attr[prop] = val 
    def __contains__(self,prop):
        return prop in self._attr

    def addProp(self,name,val,sep):
        if val is None:
            return self 
        elif isinstance(val,list):
            val = sep.join(val)
        assert isinstance(val,str), TypeError(f'Unexpected value type: {type(val)}')

        if name in self._attr:
            self._attr[name] += sep + val 
        else:
            self._attr[name] = val
        return self

    def addClass(self,val):
        return self.addProp('className',val,' ')
    def addStyle(self,val):
        return self.addProp('style',val,'; ')


# ------------------------------------------------------------------------

class Tag(QuickTag):
    """
    Overload QuickTag to implement body property as a list.
    This allows body to be extended dynamically.
    """
    def __init__(self,*arg,**kv):
        super().__init__(*arg,**kv)
        self._inline = None

    def __str__(self):
        return self.str()

    def inline(self,val):
        self._inline = bool(val)

    def body(self,val):
        if isinstance(val,list) or val is None:
            self._body = val 
        elif isinstance(val,Tag):
            self._body = [val]
        else:
            self._body = dedent(str(val),aslist=True)
        return self

    def append(self,elm):
        if elm is None:
            pass
        elif self._body is None:
            self._body = [elm]
        else:
            self._body.append(elm)
        return self

    def extend(self,elm):
        assert isinstance(elm,list), TypeError(f'Unexpected type: {type(elm)}')
        if isinstance(self._body,list):
            self._body.extend(elm)
        else:
            self._body = elm 
        return self

    def str(self,ind='',inline=None):

        name = self._name
        attr = attr2str(self._attr)

        # body
        if self._body is None:
            return f'<{name}{attr} />'
        if inline is None:
            inline = self._inline
        if inline is None:
            inline = len(self._body) == 1

        sub = ind if inline else ind+'\t'
        body = []
        for b in self._body:
            if isinstance(b,str):
                body.append(b)
            elif isinstance(b,Tag):
                body.append(b.str( ind=sub ))
            else:
                body.append(str(b))

        # output
        if inline:
            body = ''.join(body)
            return f'<{name}{attr}>{body}</{name}>'
        else:
            body = f'\n{sub}'.join(body)
            return f'<{name}{attr}>\n{sub}{body}\n{ind}</{name}>'

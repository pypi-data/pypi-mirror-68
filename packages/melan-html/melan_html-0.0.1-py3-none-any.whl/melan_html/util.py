
from .tag import QuickTag, Tag 

# ------------------------------------------------------------------------

def unquote(s):
    return s.strip('"\'')

def qtag(name,body=None,**attr):
    """
    Shorthand to define tag, and assign body.
    """
    return QuickTag(name,**attr).body(body)

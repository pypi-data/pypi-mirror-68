
from .util import file_buffer
from .parser import Parser
from .compiler import Compiler

import nxp

# ------------------------------------------------------------------------

def parse_buf( buf ):
    return nxp.parsebuf( Parser, buf )

def compile_buf( buf ):
    return Compiler().process(buf)

# ----------  =====  ----------

def parse_file( fpath, r2l=False ):
    with file_buffer(fpath,r2l) as buf:
        return parse_buf(buf)

def parse_text( text, r2l=False ):
    return parse_buf( nxp.ListBuffer(text.splitlines(True),r2l) )

def compile_file( fpath, r2l=False ):
    with file_buffer(fpath,r2l) as buf:
        return compile_buf(buf)

def compile_text( text, r2l=False ):
    return compile_buf( nxp.ListBuffer(text.splitlines(True),r2l) )

# ------------------------------------------------------------------------

class Format:
    """
    Default format, which does not modify the input text.
    Intended as a base class for derived formats in extensions.
    """
    def __init__(self,name):
        self._name = name

    @property 
    def name(self): return self._name

    def __call__(self,cpl,text):
        return text

# ------------------------------------------------------------------------

class Stack:
    """
    The stack keeps track of nested command calls, and can be used
    to enforce restrictions on such nested calls.

    For example, to ensure that only the command 'bar' can be called 
    within the body of command 'foo', call:

        stack.restrict('foo',['bar'])

    The stack is stored as a property of the compiler, and can be used
    within an extension by defining an "ini" function. Within an extension,
    the stack can be used to allow a given command to behave differently
    depending on the context. For example, the command "caption" could mean
    something different within a figure vs. a table.
    """
    def __init__(self,cpl):
        self._cpl = cpl
        self._indoc = False
        self._stack = []
        self._restrict = {}

        cpl.subscribe( 'doc.begin', self._doc_begin )
        cpl.subscribe( 'doc.end', self._doc_end )
        cpl.subscribe( 'cmd.begin', self._cmd_begin )
        cpl.subscribe( 'cmd.end', self._cmd_end )

    @property 
    def indoc(self): return self._indoc
    @property 
    def scope(self): return self._stack[-1]
    @property 
    def parent(self): return self._stack[-2]

    def __len__(self): return len(self._stack)
    def __getitem__(self,key): return self._stack[key]

    def restrict(self,cmd,allowed):
        self._restrict[cmd] = set(allowed)

    def _pop(self,name):
        if not self._indoc: return
        assert self.scope == name, RuntimeError(f'[bug] Scope {name} ended before {self.scope}.')
        self._stack.pop()

    def _push(self,name):
        if not self._indoc: return
        try:
            s = self.scope
            r = self._restrict[s]
        except:
            self._stack.append(name)
            return # either no scope, or no restriction

        assert name in r, RuntimeError(f'Command {name} not allowed in scope {s}.')
        self._stack.append(name)

    def _doc_begin(self):
        self._indoc = True
        self._push('@doc')

    def _doc_end(self):
        self._pop('@doc')
        self._indoc = False

    def _cmd_begin(self,name,pos):
        self._push(name)

    def _cmd_end(self,name,pos):
        self._pop(name)
    
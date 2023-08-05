
import os 
import re
import nxp
import math
from contextlib import contextmanager

# ------------------------------------------------------------------------

@contextmanager
def file_buffer( fpath, r2l=False ):
    """
    Create FileBuffer and move to parent folder.
    see: https://stackoverflow.com/a/13847807/472610
    """
    buf = nxp.FileBuffer(fpath,r2l)
    prev = os.getcwd()
    os.chdir(os.path.dirname(fpath))
    try: 
        yield buf 
    finally:
        os.chdir(prev)

def _indent_length(line):
    L = len(re.match(r'^\s*',line)[0])
    return L if L < len(line) else math.inf

def splitlines(text):
    """
    str.splitlines doesn not behave well for empty strings; this function does.
    """
    return re.split( r'\r?\n', text )

def dedent(body,aslist=False):
    """
    Remove first/last line if they are whitespace, and remove common leading 
    whitespace from remaining lines.
    """

    # split into lines
    lines = splitlines(body)
    if len(lines) > 1:

        # remove first/last white lines
        first = 1
        if len(lines[0].strip()) == 0: 
            lines.pop(0)
            first = 0
        if len(lines[-1].strip()) == 0:
            lines.pop()

        # process the remaining lines
        if len(lines) > first: 
            indent = min([ _indent_length(line) for line in lines[first:] ])
            if 0 < indent < math.inf: # not all blank lines
                for k,line in enumerate(lines[first:]):
                    lines[first+k] = line[indent:]

    return lines if aslist else '\n'.join(lines)

'''
Copyright (C) 2011 by Steven Hiscocks

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
import sys
import subprocess
import warnings

_formats = ['jpg', 'pdf', 'png', 'ps', 'svg', 'xdot']
_progs = ['dot', 'neato', 'twopi', 'circo', 'fdp', 'sfdp']

class GraphvizError(Exception):
    pass
class GraphvizWarning(Warning):
    pass

def graphviz(dot, prog='dot', format_='png'):
    '''Process 'dot' input via 'prog' and return stdout in 'format'.'''
    if prog not in _progs:
        raise GraphvizError("Invalid Graphviz Program: %s" % prog)
    if format_ not in _formats:
        raise GraphvizError("Invalid output format: %s" % format_)
    gv_process = subprocess.Popen(
        [prog, '-T%s' % format_], stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=True)
    if sys.version_info[0] == 3:
        dot = bytes(dot, 'utf-8')
    output, error = gv_process.communicate(input=dot)
    if gv_process.returncode != 0:
        raise GraphvizError(':'.join(str(error).split(':')[1:]))
    elif error:
        warnings.warn(str(error).partition(':')[2].strip(), GraphvizWarning)
    return output

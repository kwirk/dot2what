#!/usr/bin/env python
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
# Standard
import warnings
import mimetypes
import re

# FOSS
import bottle

# Custom
from graphviz import graphviz, GraphvizError, GraphvizWarning
warnings.simplefilter('ignore', GraphvizWarning)

app = bottle.Bottle()

def index():
    '''Returns index page with input form'''
    return """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>dot2what</title>
    </head>
    <body>
        <h1>dot...</h1>
        <form action="%s" method="post">
            <p>
                <textarea name="text" rows=30 cols=100></textarea>
            </p>
            <p>
                to what?:
                <input type="radio" name="format" value="png" checked>png
                <input type="radio" name="format" value="jpg">jpg
                <input type="radio" name="format" value="svg">svg
                <input type="radio" name="format" value="pdf">pdf
                <input type="radio" name="format" value="ps">ps
                <input type="radio" name="format" value="xdot">xdot
            </p>
            <p>
                with what?:
                <input type="radio" name="prog" value="dot" checked>dot
                <input type="radio" name="prog" value="neato">neato
                <input type="radio" name="prog" value="twopi">twopi
                <input type="radio" name="prog" value="circo">circo
                <input type="radio" name="prog" value="fdp">fdp
                <input type="radio" name="prog" value="sfdp">sfdp
            </p>
            <p>
                <input type="submit" value="Download">
            </p>
        </form>
        <h4>Notes:</h4>
        <ul>
            <li>Attributes that refer to local files (e.g. image, shapefile) are automatically removed</li>
        </ul>
    </body>
</html>""" % app.get_url("dot2_post")

def strip_external(text):
    '''Removes attributes that access external files for security'''
    def repl(match):
        if match.group(1) == "fontname" and '/' not in match.group(0):
            return match.group(0)
        elif match.group('sqbr'):
            return "]"
        else:
            return ""
    text = re.sub(r'''(?ix)(image|imagepath|shapefile|fontpath|fontname)=
                      (?P<quote>")?.+?(?(quote)")(,|(?P<sqbr>]))''',
                  repl, text)
    text = re.sub(r'(?i)<img +src=.*?".+?" */>', "", text)
    return text

@app.route('/', method=['GET','POST'], name="dot2_post")
@app.route('/<prog:re:[a-z]+>', method=['GET','POST'])
@app.route('/<prog:re:[a-z]+>2<format_:re:[a-z]+>', method=['GET','POST'])
@app.route('/<prog:re:[a-z]+>.<format_:re:[a-z]+>', method=['GET','POST'])
def dot2(prog=None, format_=None):
    '''Main dot2what conversion requests'''
    if bottle.request.method == 'POST':
        request_data = bottle.request.forms
    else: # Should be GET
        request_data = bottle.request.query

    if not prog or prog == "dot": # dot can be used as a generic term
        prog = request_data.get('prog', prog) # therefore allow override
    if not format_:
        format_ = request_data.get('format')
    text = request_data.get('text') # DOT text

    if not prog and not format_ and not text:
        return index() # Blank request, therefore return index page
    elif not text: #Incase of '' text that will not cause graphviz to error
        raise bottle.HTTPError(400, "Invalid DOT Input")

    try:
        output = graphviz(strip_external(text), prog=prog, format_=format_)
    except (GraphvizError, GraphvizWarning) as err:
        raise bottle.HTTPError(400, "GraphvizError: %s" % str(err))

    mimetype, encoding = mimetypes.guess_type(' .%s' % format_)
    if mimetype: bottle.response['Content-Type'] = mimetype
    if bottle.request.method == 'POST':
        bottle.response['Content-Disposition'] = \
            "attachment; filename=dot2.%s" % format_
    return output

if __name__ == "__main__":
    bottle.run(app, host='localhost', port=8080, reloader=True)

========
dot2what
========

On-line DOT graph description language to image converter using graphviz

Usage
-----
dot2what can be run with Bottle's development server by executing::

    python dot2what.py' which

dot2what can also be run using Bottle's WSGI interface by importing 'app' as 'application'::

    from dot2what import app as application

Requirements
------------
- python >= 2.6 (including python 3)
- `bottlepy <http://bottlepy.org/>`_ >= 0.10
- `graphviz <http://www.graphviz.org/>`_

License
-------
dot2what is released under the MIT License

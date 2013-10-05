#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Usage: pyplotter <numbers>...

Examples:
  pyplotter 13 50 43 21 85 100

Options:
    -h --help     Show help.
    -v --version  Show version.
"""

from docopt import docopt
from pyplotter import Graph, Plotter
VERSION = (0,0,1)

def run():
    version = ".".join(str(x) for x in VERSION)
    arguments = docopt(__doc__, version=version)
    numbers = arguments.get('<numbers>', None)
    if numbers:
        try:
            numbers = map(int, numbers)
            graph = Graph(data=numbers)
            Plotter.plot(graph)
        except ValueError, e:
            print e

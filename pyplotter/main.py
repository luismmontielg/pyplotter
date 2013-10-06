#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
pyplotter

Usage:
  pyplotter [--] <numbers>... [--show-min-max --padding=<padding> --title=<title> --height=<height>]
  pyplotter -h | --help
  pyplotter --version

Examples:
  pyplotter 13 50 43 21 85 100

Options:
    -h --help     Show this scren.
    -v --version  Show version.
"""

from docopt import docopt
from pyplotter import Graph, Plotter
VERSION = (0,0,2)

def run():
    version = ".".join(str(x) for x in VERSION)

    arguments = docopt(__doc__, version=version)
    numbers = arguments.get('<numbers>')
    padding = arguments.get('--padding')
    show_min_max = arguments.get('--show-min-max', False)
    title = arguments.get('--title')
    height = arguments.get('--height')

    if numbers:
        kwargs = {}
        try:
            kwargs['show_min_max'] = show_min_max
            kwargs['height'] = int(height or 2)
            kwargs['padding'] = int(padding or 0)
            graph = Graph(data=map(int, numbers), title=title)
            kwargs['graph'] = graph
            Plotter.plot(**kwargs)
        except ValueError, e:
            print e

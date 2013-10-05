#-*- coding: utf-8 -*-
from pyplotter import __version__

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    import subprocess
    def convert(source, from_format, to_format):
        p = subprocess.Popen(['pandoc', '--from=' + from_format, '--to=' + to_format],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )
        if sys.version_info[0] == 3:
            return p.communicate(bytes(source, 'UTF-8'))[0]
        return p.communicate(source)[0]
    readme = open('README.md').read() # might want to use "with" to make sure it gets closed
    long_description = convert(readme, 'markdown', 'rst')
except (OSError, IOError, ImportError) as e:
    try:
        long_description = open('README.md').read()
    except (IOError):
        long_description = ''

dependencies = []

def publish():
    os.system("python setup.py sdist upload")

if sys.argv[-1] == "publish":
    publish()
    sys.exit()

setup(
    name='pyplotter',
    version=".".join(str(x) for x in __version__),
    description='Command line bar graphs',
    long_description=long_description,
    url='http://www.github.com/luismmontielg/pyplotter',
    license="MIT License",
    author='Luis Montiel',
    author_email='luismmontielg@gmail.com',
    install_requires=dependencies,
    packages=['pyplotter'],
    entry_points={
        'console_scripts': [
            'pyplotter=pyplotter.main:run'
        ],
    },
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
)

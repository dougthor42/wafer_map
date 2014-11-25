# -*- coding: utf-8 -*-
"""
@name:          new_program.py
@vers:          0.1.0
@author:        dthor
@created:       Tue Nov 25 11:03:03 2014
@descr:         A new file

Usage:
    new_program.py

Options:
    -h --help           # Show this screen.
    --version           # Show version.
"""

from __future__ import print_function, division, absolute_import
from __future__ import unicode_literals
from docopt import docopt

__author__ = "Douglas Thor"
__version__ = "v0.1.0"


def main():
    """ Main Code """
    docopt(__doc__, version=__version__)


if __name__ == "__main__":
    main()

#!/bin/env python

'''
usage:
 genie r2 --r1=FILE [options] [--dry-run]

options:
 --r1=FILE     a file
 --out=PREFIX  outname prefix [default: r2]
 --nojob       if front end
 --dry-run
 
'''

from docopt import docopt
import sys
sys.path.insert(1, sys.path[0] + '/../../library')
import md

if __name__ == '__main__':
    md.main(docopt(__doc__), ['r2'])

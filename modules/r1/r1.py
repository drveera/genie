#!/bin/env python

'''
usage:
 genie r1 --fname=FILE [--out=PREFIX] [--nojob] [--dry-run]

options:
 --fname=FILE  a blank file
 --out=PREFIX  outname prefix [default: r1]
 --nojob       no job
 --dry-run     dry run

'''

from docopt import docopt
import sys
sys.path.insert(1, sys.path[0] + '/../../library')
import md

if __name__ == '__main__':
    md.main(docopt(__doc__), ['r1'])

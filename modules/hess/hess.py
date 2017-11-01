#!/bin/env python

'''
usage:
 genie hess [options] <sumstat>

options:
 --out=PREFIX        outname prefix [default: genie_gsmr]
 --nojob             run on front end
 --dry-run           dry run
 <sumstat>           sumstat files. Split by chromosome, filename with * in place of chr number.

'''

from docopt import docopt
import sys
sys.path.insert(1, sys.path[0] + '/../../library')
import md

if __name__ == '__main__':
    md.main(docopt(__doc__), ['hess'])


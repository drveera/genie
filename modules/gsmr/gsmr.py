#!/bin/env python

'''
usage:
 genie gsmr [options] <sum1> <sum2>

options:
 --out=PREFIX        Outname prefix [default: genie_gsmr]
 --nojob             if front end
 --dry-run            dry run

'''

from docopt import docopt
import sys
sys.path.insert(1, sys.path[0] + '/../../library')
import md

arguments = docopt(__doc__)
if __name__ == '__main__':
    md.main(arguments,['gsmr'])


#!/bin/env python

'''genie rohs <command> <arguments>


usage:
    genie rohs identify [--out=PREFIX] [--nojob] <plink-data>
    genie rohs analyze [--out=PREFIX] [--indivfile=FILe] [--missfile=FILE] [--covfile=FILE] [--pcfile=FILE] <phenofile>

options:
    --out=PREFIX         outname prefix [default: rohs]
    --indivfile=FILE     indiv file
    --missfile=FILE      miss file
    --covfile=FILE       covar file
    --pcfile=FILE        pc file
    --phenofile=FILE     phenotype file
    --nojob              run on the front end
'''

from docopt import docopt
import sys
sys.path.insert(1, sys.path[0] + '/../../library')
import md

if __name__ == '__main__':
    md.main(docopt(__doc__), ['analyze', 'identify'])


#!/bin/env python

'''genie rohs <command> <arguments>

usage:
    genie rohs analyze [options] [--]

options:
    --out=DIR            output directory [default: rohs]
    --indivfile=FILE     indiv file [default: |resources/rohs/data.hom.indiv]
    --missfile=FILE      miss file [default: |resources/rohs/pruned.imiss]
    --covfile=FILE       covar file [default: |resources/rohs/covar_uni.ssv]
    --pcfile=FILE        pc file
    --phenofile=FILE     phenotype file
    --nojob              if you want to run in front end
'''

from docopt import docopt
import sys
sys.path.insert(1, sys.path[0] + '/../../library')
import md

if __name__ == '__main__':
    md.main(docopt(__doc__), ['analyze'])


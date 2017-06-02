#!/bin/env python

'''

usage:
 eqtl fusion [options] --sumstats=FILE 

options:
 --sumstats=FILE       summary statistics file or .list 
 --weights=FILE        gene expression weights file or .list [default: |resources/fusion/weights.list]
 --chr=NUMBER          chromosome number
 --out=PREFIX          output prefix [default: genie_fusion]
 --daner               if using daner (ricopilli) format
 --Nsamples=NUMBER     if not using --daner, specifiy the sample size [default: 10000] 
 --nojob               nojob
 --dry-run             dry run
 --njobs=NUMBER    number of parallel jobs if running in front node [default: 1]
 --other=ARGS      other arguments to pass to munge
 
'''

from docopt import docopt
import sys
sys.path.insert(1, sys.path[0] + '/../../../library')
import md
from md import process_list

arguments = docopt(__doc__)
if __name__ == '__main__':
    md.main(arguments,['fusion'])

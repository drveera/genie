#!/bin/env


'''
usage:
 ldsc munge [options] --sumstats=FILE

options:
 --sumstats=FILE     daner formatted summary file
 --out=PREFIX        outname prefix [default: out]
 --Nsamples=NUMBER   sample size
 --daner             if using daner format
 --nojob             run front end
 --dry-run           just see the analysis plan but not run

'''
from docopt import docopt
import sys
sys.path.insert(1, sys.path[0] + '/../../../library')
import md
from md import process_list

arguments = docopt(__doc__)
if __name__ == '__main__':
    md.main(arguments,['munge'])

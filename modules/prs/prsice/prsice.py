#!/bin/env python

'''

usage:
 prs prsice [options] --base=FILE --target=FILE 

options:
 --base=FILE       training sample
 --target=FILE     target sample
 --pheno=FILE      external pheno file
 --slower=NUMBER   lower limit  [default: 0]
 --supper=NUMBER   upper limit [default: 0.5]
 --sinc=NUMBER     p-value increments  [default: 0.01]
 --out=PREFIX      outname prefix [default: prs]
 --covary          if covariates to be adjusted
 --clump           if clumping need to be done
 --quantitative    if using quantitative target  
 --nojob           if should be run in front end
 --dry-run         dry run

'''
from docopt import docopt
import sys
sys.path.insert(1, sys.path[0] + '/../../../library')
import md

arguments = docopt(__doc__)
if __name__ == '__main__':
    md.main(arguments,['prsice'])

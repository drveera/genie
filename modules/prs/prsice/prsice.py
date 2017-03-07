#!/bin/env python

'''

usage:
 prs prsice [options] --base=FILE --target=FILE --pheno=FILE 

options:
 --base=FILE       training sample
 --target=FILE     target sample
 --pheno=FILE      phenotype file of target sample
 --slower=NUMBER   if slower  [default: 0]
 --sinc=NUMBER     p-value increments  [default: 0.01]
 --covary          if covariates to be adjusted 

'''
from docopt import docopt
import sys
sys.path.insert(1, sys.path[0] + '/../../../library')
import md
from md import process_list

arguments = docopt(__doc__)
if __name__ == '__main__':
    print(arguments)

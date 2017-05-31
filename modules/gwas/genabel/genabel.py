#!/bin/env python

'''

usage:
 gwas genabel [options] --pheno=FILE

options:
 --pheno=FILE       phenotype file
 --covar=FILE       covariate file
 --geno=FILE        genotypefile or .list in genabel format
 --out=PREFIX       outname prefix [deafult: genabel_out]
 --nojob            run in front end
 --dry-run          just show the codes
 --njobs=NUMBER     number of parallel jobs; applicable only when running 
                    in front end

'''
from docopt import docopt
import sys
sys.path.insert(1, sys.path[0] + '/../../../library')
import md

arguments = docopt(__doc__)
if __name__ == '__main__':
    md.main(arguments,['genabel'])

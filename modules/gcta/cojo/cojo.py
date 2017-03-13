#!/bin/env python

'''
usage:
 gcta cojo (--cojo-slct | --cojo-joint | --cojo-cond=FILE ) --cojo-file=SUMMARY  [options]

options:
 --cojo-file=SUMMARY  Summary file
 --bfile=PLINK        Plink file [default: |resources/magma/g1000_eur]
 --chr=NUMBER         Chromosome number 
 --maf=NUMBER         Minor allele frequency
 --out=PREFIX         Outname prefix [default: genie_cojo]
 --extract=LIST       a file with list of SNPs
 --cojo-slct          Select multiple associated SNPs through a stepwise selection procedure
 --cojo-joint         Estimate the joint effects of a subset of SNPs
 --cojo-cond=FILE     Perform single-SNP association analyses conditional on a set of SNPs
 --nojob             if front end
 --dry-run            dry run

'''

from docopt import docopt
import sys
sys.path.insert(1, sys.path[0] + '/../../../library')
import md
from md import process_list

arguments = docopt(__doc__)
if __name__ == '__main__':
    md.main(arguments,['cojo'])

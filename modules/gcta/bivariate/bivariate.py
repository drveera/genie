#!/bin/env gcta

'''
usage:
 gcta bivariate [options] --grm=GRMFILE --pheno=FILE

options:
 --reml-bivar-nocove               exclude the residual variance
 --grm=GRMFILE                     grm file
 --pheno=FILE                      pheno file 
 --out=PREFIX                      outname prefix [default: bivariate]
 --reml-bivar-lrt-rg=NUMBER        To test for the hypothesis of fixing the genetic 
                                   correlation at a particular value, 
                                   e.g. fixing genetic correlation at -1, 0 and 1
 --reml-bivar-prevalence=NUMBERS   For a bivariate analysis of two disease traits, 
                                   specify the prevalence rates of the two diseases 
 --nojob                           if should run in front end

'''

from docopt import docopt
import sys
sys.path.insert(1, sys.path[0] + '/../../../library')
import md
from md import process_list

arguments = docopt(__doc__)
if __name__ == '__main__':
    md.main(arguments,['bivariate'])
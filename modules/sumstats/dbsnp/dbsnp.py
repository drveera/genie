#!/bin/python

'''

usage:
 sumstats dbsnp [options] --sumstats=FILE

options:
 --sumstats=FILE       summary statistics file
 --out=PREFIX          output name prefix [default: out]
 --chr=NAME            chromosome column name [default: CHR]
 --pos=NAME            position column name [default: BP]
 --ref=NAME            ref allele column name [default: A1]
 --alt=NAME            alternate allele column name [default: A2]
 --dry-run             dry run
 --nojob               if need to be run in front end

'''

from docopt import docopt
import sys
sys.path.insert(1, sys.path[0] + '/../../../library')
import md
from md import process_list

arguments = docopt(__doc__)
if __name__ == '__main__':
    md.main(arguments,['dbsnp'])

#!/bin/python

'''

usage:
 sumstats clump [options] --sumstats=FILE --ld=PLINKFILE

options:
 --sumstats=FILE     munged summary statistics file 
 --out=PREFIX        output name prefix [default: clump_out]
 --ld=PLINKFILE      plink file without extension
 --p1=NUMBER         pvalue threshold 1 [default: 1]
 --p2=NUMBER         pvalue threshold 2 [default: 1]
 --r2=NUMBER         rsquared value [default: 0.1]
 --distance=NUMBER   window distance in kb [default: 250]
 --nojob             if should run in front end
 --njobs=NUMBER      Number of parallel jobs when running in front end
 --dry-run           dry run snakemake
 --other=ARGS        other arguments to pass to plink with quotes

'''

from docopt import docopt
import sys
sys.path.insert(1, sys.path[0] + '/../../../library')
import md
from md import process_list

arguments = docopt(__doc__)
if __name__ == '__main__':
    md.main(arguments,['clump'])

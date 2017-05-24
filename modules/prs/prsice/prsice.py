#!/bin/env python

'''

usage:
 prs prsice [options] --base=FILE --target=FILE 

options:
 --base=FILE             training sample file or file.list
 --target=FILE           target sample file or file.list
 --slower=NUMBER         lower limit  [default: 0]
 --supper=NUMBER         upper limit [default: 0.5]
 --sinc=NUMBER           p-value increments  [default: 0.1]
 --out=PREFIX            outname prefix [default: prs]
 --clump                 if clumping need to be done
 --clump_p1=NUMBER       clump p1 threshold [default: 1]
 --clump_p2=NUMBER       clump p2 threshold [default: 1]
 --clump_r2=NUMBER       clump r2 threshold [default: 0.1]
 --clump_kb=NUMBER       clump distance [default: 250]
 --remove_mhc            If you want to remove MHC region 
 --nojob                 if should be run in front end
 --njobs=NUMBER          Number of parallel jobs when running in front end
 --dry-run               dry run

'''
from docopt import docopt
import sys
sys.path.insert(1, sys.path[0] + '/../../../library')
import md

arguments = docopt(__doc__)
if __name__ == '__main__':
    md.main(arguments,['prsice'])

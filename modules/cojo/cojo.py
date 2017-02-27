#!/bin/env python

'''ipsych cojo

usage:
 ipsych cojo [options] <summary-file>

options:
 --out=PREFIX       outname prefix [default: ipsych_cojo]
 --ldfile=FILE      ld reference plink-file [default: ....]
 --nsamples=NUMBER  number of samples
 --nojob            if you want to run in front end

 '''

from docopt import docopt
import md

if __name__ == '__main__':
    md.main(docopt(__doc__))

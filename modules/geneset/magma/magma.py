#!/bin/env python

'''
usage:
 geneset magma [options] <summary-file>

options:
 --out=PREFIX       outname prefix[default: output]
 --geneloc=FILE     geneloc file [default: |resources/magma/NCBI37.3.gene.loc.symbols]
 --ldfile=FILE      reference file in plink format [default: |resources/magma/g1000_eur]
 --ncol=NAME        name of the column containing the sample size [default: Neff]
 --nsamples=NUMBER  alternatively, the number of samples can be assigned like this
 --genesets=FILE    genesets file in gmt format [default: |resources/magma/gmt.list]
 --nojob            run on the front end
 --dry-run          dry run
 --njobs=NUMBER     number of parallel jobs [default: 1]
 <summary-file>     a single summary file or a text file(with extension .list) containing the list of summary files


'''

from docopt import docopt
import sys
sys.path.insert(1, sys.path[0] + '/../../../library')
import md
from md import process_list

arguments = docopt(__doc__)
if __name__ == '__main__':
    md.main(arguments, ['magma', 'vegas', 'fastbat'])


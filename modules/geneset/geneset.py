#!/bin/env python

'''ipsych geneset <command> <arguments>

usage:
 genie geneset magma [--out=PREFIX] [--geneloc=FILE] [--ldfile=FILE] [--nsamples=NUMBER] [--genesets=FILE] [--nojob] [--] <summary-file>
 genie geneset vegas [options] [--] <summary-file>
 genie geneset fastbat [options] [--] <summary-file>

options:
 --out=PREFIX       outname prefix[default: output]
 --geneloc=FILE     geneloc file [default: |resources/magma/NCBI37.3.gene.loc.formatted]
 --ldfile=FILE      reference file in plink format [default: |resources/magma/dbs1-23.bgs.merged.raw]
 --nsamples=NUMBER  number of samples [default: 10000]
 --genesets=FILE    genesets file in gmt format [default: |resources/magma/msigdb.v5.2.symbols.gmt]
 --nojob            if you want to run in front end
 <summary-file>     a single summary file or a text file(with extension .list) containing the list of summary files

'''

from docopt import docopt
import sys
sys.path.insert(1, sys.path[0] + '/../../library')
import md

if __name__ == '__main__':
    md.main(docopt(__doc__), ['magma', 'vegas', 'fastbat'])


#!/bin/env python

'''ipsych magma

usage:
 ipsych magma [options] [--] <summary-file>

options:
 --out=PREFIX       outname prefix[default: ipsych_magma]
 --geneloc=FILE     geneloc file [default: |resources/magma/NCBI37.3.gene.loc.formatted]
 --ldfile=FILE      reference file in plink format [default: |resources/magma/dbs1-23.bgs.merged.raw]
 --nsamples=NUMBER  number of samples [default: 10000]
 --genesets=FILE    genesets file in gmt format [default: |resources/magma/msigdb.v5.2.symbols.gmt]
 --nojob            if you want to run in front end

'''

from docopt import docopt
import os
import sys
import json
import md


if __name__ == '__main__':
    arguments = docopt(__doc__)

arguments = md.fix_default_arguments(arguments)

outname = arguments['--out']
configfile = outname + f'_magma.json'

with open(configfile, 'w') as outfile:
    json.dump(arguments, outfile, indent=4)

if not arguments['--nojob']:
    time = '11:59:00'
    jobscript = outname + '_magma.master.sh'
    with open(jobscript,'w') as outfile:
        outfile.write('#!/bin/sh \n' +
                      'snakemake -j 999 ' +
                      f'--configfile {configfile} ' +
                      f'--jobname {outname}.{{rulename}}.{{jobid}} ' +
                      f'--cluster \'sbatch --mem=32g --time={time}\' ' +
                      f'-s {sys.path[0]}/magma.snake \n')
    os.system(f'sbatch --time={time} {jobscript}')

else:
    os.system("snakemake -j 999 --configfile " + configfile + " -s " + sys.path[0] + "/magma.snake")


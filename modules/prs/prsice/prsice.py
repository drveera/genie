#!/bin/env python

'''

usage:
 prs prsice [options] --base=FILE --target=FILE 

options:
 --base=FILE             training sample
 --target=FILE           target sample
 --ped                   if the target sample is in ped format 
 --pheno=FILE            external pheno file
 --quantitative          if using quantitative target 
 --slower=NUMBER         lower limit  [default: 0]
 --supper=NUMBER         upper limit [default: 0.5]
 --sinc=NUMBER           p-value increments  [default: 0.01]
 --out=PREFIX            outname prefix [default: prs]

 --nocov                 if covariates not to be used
 --covar=FILE            if you have own covariate file 
 --pcs=IDS               If you have not provided covariate file, the script will calculate PCs.
                         In that case, which all pcs you'd like to adjust for, default will be C1,C2
 --pc_method=NAME        either PCA or MDS [default: MDS]

 --clump                 if clumping need to be done
 --clump_p1=NUMBER       clump p1 threshold [default: 1]
 --clump_p2=NUMBER       clump p2 threshold [default: 1]
 --clump_r2=NUMBER       clump r2 threshold [default: 0.1]
 --clump_kb=NUMBER       clump distance [default: 250]
 
 --prune                 if pruning needed to be done; remember you can use either clump or prune, not both
 --prune_kb_wind=NUMBER  window size [default: 50]
 --prune_kb_step=NUMBER  sliding window [default: 2]
 --prune_r2=NUMBER       r2 threshold for pruning [default: 0.8]
 --report_all_scores     if you need all the scores at all thresholds used
 --no_regression         If regression is not needed
 --for_meta              If coeff and SE are needed for further meta analysis
 --remove_mhc            If you want to remove MHC region 
 --nojob                 if should be run in front end
 --dry-run               dry run

'''
from docopt import docopt
import sys
sys.path.insert(1, sys.path[0] + '/../../../library')
import md

arguments = docopt(__doc__)
if __name__ == '__main__':
    md.main(arguments,['prsice'])

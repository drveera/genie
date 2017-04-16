#!/bin/env python

'''
usage:
 genie rare [options] (--vcf=FILE|--bfile=PLINKFILE) (--pheno=FILE|--fam=FILE)

options:
 --vcf=FILE                  vcf file
 --bfile=PLINKFILE           plink file without extenstion
 --pheno=FILE                plink pheno file in 2+n column(fid/iid/p1,p2..) format
 --fam=FILE                  plink fam file,  5+n column(fid,iid,motherid,fatherid,sex,p1,p2..) format
                             you can provide only either pheno or fam, not both. 
 --pheno-name=NAME           name of the pheno column to analyze
                             applicable to both --pheno and --fam arguments
 --covar=FILE                covariate file (refer to rvtest doc
                             which tests covar is applicable)) 
 --covar-name=NAMES          comma seperated list of col names in covar file to adjust                            
 -q                          if phenotype is quantitative
 --single=NAMES              comma seperated list of tests 
                             if all, write '--single=all' 
                             available-binary-tests:score,wald,exact,dominantExact,firth
                             available-q-tests:score,wald,famLRT,famscore,famGrammerGamma

 --burden=NAMES              comma seperated list of burden tests 
                             if all, write '--burden=all' 
                             available-binary-tests:cmc,zeggini,mb,fp,exactCMC,cmcWald,rarecover,cmat
                             available-q-tests:cmc,zeggini,cmcWald,famcmc,famzeggini

 --vt=NAMES                  comma seperated list of variable thresholds 
                             if all, write '--vt=all'
                             available-binary-thresholds:price
                             available-q-thresholds:price,analytic

 --kernel=NAMES             comma seperated list of kernel models
                            if all, write '--kernel=all'
                            available-binary-kernels:skat,skato
                            available-q-kernels:skat,skato,kbac,famSkat 

 --meta=NAMES               comma seperated list of meta names
                            if all, write '--meta=all'
                            available-binary-tests:score,dominant,recessive,cov
                            available-q-tests:score,dominant,recessive,cov

 --raremetal                If meta analysis of results from multiple vcf files are desired
 --geneFile=RANGE           in refFlat format
 --gene=GENENAMES           comma seperated list of GENE ids
 --out=PREFIX               outname prefix [default: rare_out]
 --nojob                    front end
 --njobs=NUMBER             number of parallel jobs if running in front end
 --dry-run                  dry run

'''

from docopt import docopt
import sys
from itertools import compress
sys.path.insert(1, sys.path[0] + '/../../library')
import md
arguments = docopt(__doc__)

if not any([
        arguments['--single'],
        arguments['--burden'],
        arguments['--vt'],
        arguments['--kernel'],
        arguments['--meta']]):
    sys.exit("Exiting; No tests requested")
stests_binary = ["score","wald","exact","dominantExact","firth"]
stests_quant = ['score','wald','famLRT','famScore','famGrammarGamma']

btests_binary = ["cmc","zeggini","mb","fp","exactCMC","cmcWald","rarecover","cmat"]
btests_quant = ["cmc","zeggini","cmcWald","famcmc","famzeggini"]

vt_binary = ['price']
vt_quant = ['price','analytic']

kernel_binary = ['skat','skato']
kernel_quant = ['skat','skato','kbac','famSkat']

meta_binary = ['score','dominant','recessive','cov']
meta_quant = ['score','dominant','recessive','cov']

def assign_all(test,allvalues):
    if 'all' in test:
        return allvalues
    else:
        return test

if arguments['--single']:
    stest = arguments['--single']
    stest = stest.split(",")

if arguments['--burden']:
    btest = arguments['--burden']
    btest = btest.split(",")

if arguments['--vt']:
    vt = arguments['--vt']
    vt = vt.split(",")

if arguments['--kernel']:
    kernel = arguments['--kernel']
    kernel = kernel.split(",")

if arguments['--meta']:
    meta = arguments['--meta']
    meta = meta.split(",")

def testcheck(ttype,test,t1,t2,):
    if arguments['-q']:
        available_tests = t1
        ptype = "quantitative"
    else:
        available_tests = t2
        ptype = "binary"
    test = assign_all(test,available_tests)
    fltr = [i not in available_tests for i in test]
    invalid_tests = list(compress(test,fltr))
    if len(invalid_tests)>0:
        print(f"Ignoring the following {ttype} as they are not valid for {ptype} phenotype:\n{invalid_tests}")
    fltr =  [i in available_tests for i in test]
    test = list(compress(test,fltr))
    if test == []:
        sys.exit(f"Stopping exection; No valid {ttype} given to further proceed")
    else:
        return test


if arguments['--single']:
    arguments['single'] = testcheck("single variant tests",stest,stests_quant,stests_binary)
else:
    arguments['single'] = None
if arguments['--burden']:
    arguments['burden'] = testcheck("burden tests", btest,btests_quant,btests_binary)
else:
    arguments['burden'] = None
if arguments['--vt']:
    arguments['vt'] = testcheck("variable thresholds", vt,vt_quant,vt_binary)
else:
    arguments['vt'] = None
    
if arguments['--kernel']:
    arguments['kernel'] = testcheck("kernel models", kernel,kernel_quant,kernel_binary)
else:
    arguments['kernel'] = None

if arguments['--meta']:
    arguments['meta'] = testcheck("meta tests",meta,meta_quant,meta_binary)
else:
    arguments['meta'] = None

if __name__ == '__main__':
    md.main(arguments,['rare'])

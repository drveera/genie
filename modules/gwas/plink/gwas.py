#!/bin/env python

"""sgwas
 
Usage:
 sgwas --dosedir=FOLDER --pheno=FILE [--out=NAME] [--covar=FILE] [--pattern=EXPR]
 sgwas (-h | --help)

Options:
 -h --help         show this screen
 --dosedir=FOLDER  folder containing the plink-dosage files 
 --pheno=FILE      phenotype file
 --out=NAME        outname [default: gwas]
 --covar=FILE      covariate file; this is optional 
 --pattern=EXPR    dose files pattern [default: *gz]

"""

from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__, version='sgwas 1.0')

##################################################################################
#save the input arguments
dosedir=arguments['--dosedir']
pattern=arguments['--pattern']
outname=arguments['--out']
pheno=arguments['--pheno']
covar=arguments['--covar']
##################################################################################


##################################################################################
#create the doselist
import os
import os.path
cd=os.getcwd()
os.chdir(dosedir)
os.system("ls {0} | sed s/.gz//g > {1}/{2}.dose.list".format(pattern,cd,outname))
os.chdir(cd)
##################################################################################


##################################################################################
# create config.file in json format
import json
import sys
scon = {}
scon['doselist'] = outname + '.dose.list'
scon['pheno'] = pheno
scon['covar'] = covar
scon['dosedir'] = dosedir
scon['outname'] = outname
with open(outname + '.sgwas.config.json', 'w') as outfile:  
    json.dump(scon, outfile, indent = 4)
##################################################################################


##################################################################################
# create cluster.config file
ccon= {}
ccon['__default__'] = {}
ccon['__default__']['mem'] = '16g'
ccon['__default__']['cores'] = '1'
ccon['__default__']['time'] = '10:00:00'
ccon['__default__']['err'] = outname + ".err"
ccon['__default__']['out'] = outname + ".out"




with open(outname + '.sgwas.cluster.json', 'w') as outfile:
    json.dump(ccon,outfile, indent = 4)
##################################################################################


# write master
with open(outname + ".sgwas.master.sh",'w') as outfile:
    outfile.write("#!/bin/sh \n")
    outfile.write("source ~/.bashrc \n")
    outfile.write("snakemake -j 1000000 ")
    outfile.write("--configfile {0}.sgwas.config.json ".format(outname))
    outfile.write("--cluster-config {0}.sgwas.cluster.json ".format(outname))
    outfile.write("--jobname " + "'" + outname + "_sgwas" + ".{rulename}.{jobid}' ")
    outfile.write("--cluster 'sbatch --mem={cluster.mem} -c {cluster.cores} --time={cluster.time} -e {cluster.err} -o {cluster.out} ' ")
    outfile.write(" -s " + sys.path[0] + "/gwas.snake \n")
    

# submit job
os.system("sbatch --time=480:00:00 " + outname + ".gwas.master.sh")


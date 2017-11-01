import sys
import os
from os.path import basename
import json
import re

methoddir = sys.path[0]
#here we assume that the method is always 2 levels down mainfolder, ex, ./module/method/.
#maindir = methoddir + "/../../../"
#so we grep search genie instead
maindir = re.search(r'.*genie/',methoddir).group()

def main(args, methods):
    method = next(arg for arg in methods if arg in args and args[arg])

    args = process_arguments(args)
    outfolder = f"genie_{method}/{args['--out']}"
    pfix = f"{outfolder}/{args['--out']}"

    args[f"pfix_{method}"] = pfix
    args['--outfolder'] = outfolder

    debugdir = f"_debug/{outfolder}"

    os.makedirs(debugdir, exist_ok=True)
    os.makedirs(debugdir + '/out', exist_ok=True)
    os.makedirs(debugdir + '/error', exist_ok=True)
    os.makedirs(outfolder, exist_ok=True)

    write_config(args, debugdir)
    try:
        if args['--nojob']:
            if args['--njobs']:
                njobs = args['--njobs']
            else:
                njobs = 1
        else:
            njobs = 100000
    except LookupError:
        if args['--nojob']:
            njobs = 1
        else:
            njobs = 100000
        

    cmds = f"snakemake -j {njobs} --use-conda --keep-going " \
          f"--cluster-config {maindir}/library/cluster.json " \
          f"--configfile {debugdir}/config.json " \
          f"--nolock " \
          f"-s {methoddir}/{method}.snake"

    if args['--dry-run']:
        os.system(cmds + " --printshellcmds")
    elif args['--nojob']:
        os.system(cmds)
    else:
        run_job(debugdir, args['--out'], cmds)


def process_arguments(args):
    for arg, val in args.items():
        if isinstance(val, str) and '|' in val:
            args[arg] = maindir + '/' + val[1:]
    return args


def write_config(args, debugdir):
    with open(debugdir + '/config.json', 'w') as outfile:
        json.dump(args, outfile, indent=4)


def run_job(debugdir, outname, scmds):

    cmds = f"#!/bin/sh \n {scmds} " \
           f"--jobname {outname}.{{rulename}}.{{jobid}} " \
           f"--cluster 'sbatch -e {debugdir}/error/slurm-%A_%a.out.error -o {debugdir}/out/slurm-%A_%a.out " \
           f"--mem={{cluster.mem}} --time={{cluster.time}} -c {{cluster.cores}}' " 

    jobscript = debugdir + '/jobscript.sh'
    with open(jobscript, 'w') as outfile:
        outfile.write(cmds)

    os.system(f"sbatch --time=12:00:00 -e {debugdir}/master.error -o {debugdir}/master.out {jobscript}")


def process_list(argument):
    if ".list" in argument:
        d = {}
        argument_list = [x.strip() for x in list(open(argument))]
        argument_list = [x.split(" ") for x in argument_list]
        for i in argument_list:
            d[basename(i[0])] = i
        return(d)
    else:
        argument_list = argument.split(" ")
        d = {}
        d[basename(argument_list[0])] = argument_list
        return(d)

def flen(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

    

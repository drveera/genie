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
    os.makedirs(outfolder, exist_ok=True)

    write_config(args, debugdir)

    cmds = "snakemake -j 999 " \
          f"--cluster-config {maindir}/library/cluster.json " \
          f"--configfile {debugdir}/config.json " \
          f"--nolock " \
          f"-s {methoddir}/{method}.snake"

    if args['--dry-run']:
        os.system(cmds + " -n")
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
           f"--cluster 'sbatch -e {debugdir}/e.error -o {debugdir}/o.out " \
           f"--mem={{cluster.mem}} --time={{cluster.time}} -c {{cluster.cores}}' " 

    jobscript = debugdir + '/jobscript.sh'
    with open(jobscript, 'w') as outfile:
        outfile.write(cmds)

    os.system(f"sbatch --time=12:00:00 -e {debugdir}/master.error -o {debugdir}/master.out {jobscript}")


def process_list(argument, outfolder):
        if ".list" in argument:
            os.makedirs(f"{outfolder}/._infiles", exist_ok = True)
            argument_list = [x.strip() for x in list(open(argument))]
            for x in argument_list:
                dest=f"{outfolder}/._infiles/{basename(x)}"
                if not os.path.lexists(dest):
                    os.symlink(x,dest)               
            return [basename(x) for x in argument_list]

        else:
            dest=f"{outfolder}/._infiles/{basename(argument)}"
            os.makedirs(f"{outfolder}/._infiles", exist_ok = True)
            if not os.path.lexists(dest):
                os.symlink(argument, dest)
            return [basename(argument)]


import sys
import os
import json

methoddir = sys.path[0]
maindir = methoddir + "/../../"


def main(args, methods):
    method = next(arg for arg in methods if arg in args and args[arg])

    args = process_arguments(args)

    outfolder = f"genie_{method}"
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

    if args['--nojob']:
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
           f"--cluster 'sbatch -e {debugdir}/e.error -o {debugdir}/o.out ' " \

    jobscript = debugdir + '/jobscript.sh'
    with open(jobscript, 'w') as outfile:
        outfile.write(cmds)

    os.system(f"sbatch --time=12:00:00 -e {debugdir}/master.error -o {debugdir}/master.out {jobscript}")


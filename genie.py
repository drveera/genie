#!/bin/env python

## this main docopt file. This will call all the sub docopt files based on the commands.

'''genie

usage:
 genie <command> [<args>...]

The following commands are available:
COMMAND   DESCRIPTION
gwas      run gwas
geneset   run gene/geneset analysis using gwas summary file
rohs      run analysis of runs of homozygosity
prs       run polygenic risk score analysis
gcta      run GCTA analyses

See 'genie <command> --help' for more information on a specific command.
For example, type 'ipsych geneset --help'

'''

from subprocess import call
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__, options_first=True)

argv = [arguments['<command>']] + arguments['<args>']

import sys

########################################################################################################
#CHECK IF VALID COMMAND
command = arguments['<command>']
modules = ['gwas', 'geneset', 'rohs', 'cojo', 'prs', 'r1', 'r2','recipe','gcta']
if command not in modules:
    exit(command + " is a not valid command")
########################################################################################################


########################################################################################################
# CALL THE SUB MODULE
exit(call(['python',sys.path[0] + '/modules/' + command + '/' + command + '.py'] + argv))
########################################################################################################



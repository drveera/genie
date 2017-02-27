#!/bin/env python

## this main docopt file. This will call all the sub docopt files based on the commands.

'''ipsych

usage:
 genie <command> [<args>...]

The following commands are available:
COMMAND   DESCRIPTION
gwas      run gwas
geneset   run gene/geneset analysis using gwas summary file
cojo      run gcta conditional and joint analysis using summary file
rohs      run analysis of runs of homozygosity

See 'ipsych help <command> --help' for more information on a specific command.
For example, type 'ipsych magma --help'

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
modules = ['gwas', 'geneset', 'rohs', 'cojo']
if command not in modules:
    exit(command + " is a not valid command")
########################################################################################################


########################################################################################################
# CALL THE SUB MODULE
exit(call(['python',sys.path[0] + '/modules/' + command + '/' + command + '.py'] + argv))
########################################################################################################



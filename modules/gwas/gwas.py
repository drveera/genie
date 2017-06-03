#!/bin/env python

'''

usage:
 genie gwas <method> [<args>...]

The following prs methods are available:

COMMAND  DESCRIPTION
genabel  run gwas using R GenABEL package

type 'genie gwas <method> --help' for more information on specific command
For example, type 'genie gwas genabel --help'

'''

########################################################################################################
#IMPORTS
from subprocess import call
from docopt import docopt
import sys
########################################################################################################

########################################################################################################
#DOCOPT
if __name__ == '__main__':
    arguments = docopt(__doc__, options_first=True)
argv = [arguments['<method>']] + arguments['<args>']
########################################################################################################

########################################################################################################
# CHECK IF METHOD IS VALID
method = arguments['<method>']
gwasmethods = ['genabel','plink','-h','--help']
if method not in gwasmethods:
    exit(method + " is not valid")
########################################################################################################


########################################################################################################
# HELP MESSAGE
if method == '-h' or method == '--help':
    exit(print(__doc__))
########################################################################################################


########################################################################################################
# CALL THE METHOD
exit(call(['python', sys.path[0] + "/" + method + "/" + method + '.py'] + argv))
########################################################################################################

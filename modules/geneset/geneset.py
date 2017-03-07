#!/bin/env python

'''

usage:
 genie geneset <method> [<args>...]

The following geneset methods are available:

COMMAND DESCRIPTION
magma
vegas
fastbat
pascal

type 'genie geneset <method> --help' for more information on specific method
For example, type 'genie geneset magma --help'

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
genemethods = ['magma', 'vegas', 'fastbat','pascal','-h','--help']
if method not in genemethods:
    exit(method + " is not available")
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

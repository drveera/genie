#!/bin/env python

''' genie gcta 

usage:
 genie gcta <method> [<args>...]

The following methods are available:

COMMAND     DESCRIPTION
variance    estimate heritability
bivariate   GCTA bivariate GREML analysis
cojo        conditional and joint genome-wide association analysis


type "genie gcta <method> --help for more information on specific method
For example, type 'genie gcta bivariate --help'

'''

from subprocess import call
from docopt import docopt
import sys

if __name__ == '__main__':
    arguments = docopt(__doc__, options_first = True)
argv = [arguments['<method>']] + arguments['<args>']
########################################################################################################

########################################################################################################
# CHECK IF METHOD IS VALID
method = arguments['<method>']
methods = ['variance','bivariate','cojo','-h','--help']
if method not in methods:
    exit("The gcta method " + method +  " is not available")
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

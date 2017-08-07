#!/bin/python

'''genie utils

usage:
 genie ldsc <method> [<args>...]

The following methods are available:

COMMAND     DESCRIPTION
munge       munge using ldsc munge script

type 'genie sumstats <method> --help' for more information on specific method
For example, type 'genie ldsc --help'

'''

from subprocess import call
from docopt import docopt
import sys

if __name__ == '__main__':
    arguments = docopt(__doc__, options_first = True)
argv = [arguments['<method>']] + arguments['<args>']


# CHECK IF METHOD IS VALID
method = arguments['<method>']
methods = ['munge','annotate','partition','-h','--help']
if method not in methods:
    exit("The ldsc method " + method +  " is not available")

# HELP MESSAGE
if method == '-h' or method == '--help':
    exit(print(__doc__))

# CALL THE METHOD
exit(call(['python', sys.path[0] + "/" + method + "/" + method + '.py'] + argv))

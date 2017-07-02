#!/bin/python

'''genie eqtl

usage:
 genie eqtl <method> [<args>...]

The following methods are available:

COMMAND DESCRIPTION
fusion  run fusion


type 'genie eqtl <method> --help' for more information on specific method
For example, type 'genie eqtl fusion --help'

'''

from subprocess import call
from docopt import docopt
import sys

if __name__ == '__main__':
    arguments = docopt(__doc__, options_first = True)
argv = [arguments['<method>']] + arguments['<args>']


# CHECK IF METHOD IS VALID
method = arguments['<method>']
methods = ['fusion','predixcan','metaxcan','gtx','-h','--help']
if method not in methods:
    exit("The eqtl method " + method +  " is not available")

# HELP MESSAGE
if method == '-h' or method == '--help':
    exit(print(__doc__))

# CALL THE METHOD
exit(call(['python', sys.path[0] + "/" + method + "/" + method + '.py'] + argv))

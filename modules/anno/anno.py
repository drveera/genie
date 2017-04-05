#!/bin/python

'''genie anno

usage:
 genie anno <method> [<args>...]

The following methods are available:

COMMAND DESCRIPTION
annovar  run annovar


type 'genie anno <method> --help' for more information on specific method
For example, type 'genie anno annovar --help'

'''

from subprocess import call
from docopt import docopt
import sys

if __name__ == '__main__':
    arguments = docopt(__doc__, options_first = True)
argv = [arguments['<method>']] + arguments['<args>']


# CHECK IF METHOD IS VALID
method = arguments['<method>']
methods = ['annovar','-h','--help']
if method not in methods:
    exit("The anno method " + method +  " is not available")

# HELP MESSAGE
if method == '-h' or method == '--help':
    exit(print(__doc__))

# CALL THE METHOD
exit(call(['python', sys.path[0] + "/" + method + "/" + method + '.py'] + argv))

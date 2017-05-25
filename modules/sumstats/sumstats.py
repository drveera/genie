#!/bin/python

'''genie utils

usage:
 genie sumstats <method> [<args>...]

The following methods are available:

COMMAND     DESCRIPTION
dbsnp       update snp names with dbsnp rsids 
clump       clump the snps 


type 'genie sumstats <method> --help' for more information on specific method
For example, type 'genie sumstats --help'

'''

from subprocess import call
from docopt import docopt
import sys

if __name__ == '__main__':
    arguments = docopt(__doc__, options_first = True)
argv = [arguments['<method>']] + arguments['<args>']


# CHECK IF METHOD IS VALID
method = arguments['<method>']
methods = ['dbsnp','clump','-h','--help']
if method not in methods:
    exit("The sumstats method " + method +  " is not available")

# HELP MESSAGE
if method == '-h' or method == '--help':
    exit(print(__doc__))

# CALL THE METHOD
exit(call(['python', sys.path[0] + "/" + method + "/" + method + '.py'] + argv))

#!/bin/env python

'''
usage:
 genie recipe prepare [--list=FILE] (--out=PREFIX) [<method>...] 
 genie recipe run --config=FILE 

options:
 <method>       two or more method names
 --out=PREFIX   prefix outname
 --list=FILE    instead of passing method names as arguments, provide a file with the list of methods each in a seperate line
 --config=FILE  provide the config file to run the recipe

'''
from docopt import docopt
import json
from collections import ChainMap
import sys

#import sys
#sys.path.insert(1, sys.path[0] + '/../../library')
#import md

arguments = docopt(__doc__)
outstring = arguments['--out']

def prepare_recipe(arguments):
    if arguments['--list'] is not None:
        methods_list = [x.strip() for x in list(open(arguments['--list']))]        
    else:
        methods_list = arguments['<method>']
    arguments['--mlist'] = methods_list
    #load the json files
    d = [json.load(open(f"{sys.path[0]}/{i}.json")) for i in methods_list]
    d = [update_inputs(x) for x in d]
    #merge
    d = dict(ChainMap(*d))
    ## this has to be changed
    d['all_recipe_out'] = f"genie_r2/{outstring}/{outstring}_part1"
    #write json
    with open("recipe.json",'w') as outfile:
        json.dump(d, outfile, indent = 4)

def update_inputs(json):
    method = json['_method'] 
    json[f"--pfix_{method}"] = f"genie_{method}/{outstring}/{outstring}"
    if not json['pipein'] == 'None':
        json[json['pipe_input']] = [findout(x,json['pipe_output']) for x in json['pipein']]
    return json

def findout(method,ext):    
    return f"genie_{method}/{outstring}/{outstring}{ext}"
            
if __name__ == '__main__':
    prepare_recipe(arguments)
        

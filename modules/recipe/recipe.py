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
    write_snake(methods_list)
    arguments['--mlist'] = methods_list
    #load the json files
    d = [json.load(open(f"{sys.path[0]}/{i}.json")) for i in methods_list]
    d = [update_inputs(x,methods_list) for x in d]
    #merge
    d = dict(ChainMap(*d))
    ## this has to be changed
    d['all_recipe_out'] = f"genie_r2/{outstring}/{outstring}_part1"
    #write json
    with open("recipe.json",'w') as outfile:
        json.dump(d, outfile, indent = 4)

def update_inputs(jsn,methods_list):
    method = jsn['_method'] 
    jsn[f"pfix_{method}"] = f"genie_{method}/{outstring}/{outstring}"
    if not jsn['pipein_methods'] == 'None':
        pi = []
        for x in jsn['pipein_methods']:            
            if x in methods_list:
                x_json = json.load(open(f"{sys.path[0]}/{x}.json"))
                for y in [x_json['pipe_output_suffix']]:
                    for wcard in x_json['wcard']:
                        pi.append(findout(x,wcard,y)) 
#                pi.append([findout(x,y) for y in [x_json['pipe_output_suffix']]])
        jsn[jsn['pipe_input']] = pi
        #json[json['pipe_input']] = [findout(x,json['pipe_output_suffix']) for x in json['pipein']]
    return jsn

def findout(method,wcard,ext):    
    return f"genie_{method}/{outstring}/{outstring}_{{{wcard}}}{ext}"

def write_snake(methods_list):
    with open("recipe.snake","w") as snake:
        for x in methods_list:
            snake.write(f"include: '{sys.path[0]}/../{x}/{x}.snake' \n")
        snake.write(f"rule recipe_all: \n")
        snake.write(f"\t input: \n")
        for x in methods_list:
            x_json = json.load(open(f"{sys.path[0]}/{x}.json"))            
            x_out = [findout(x,wcard,y) for y in x_json["all_out_suffix"] for wcard in x_json["wcard"]]
            for y in x_out:
                snake.write(f"\t \t '{y}', \n")
        
            
if __name__ == '__main__':
    prepare_recipe(arguments)

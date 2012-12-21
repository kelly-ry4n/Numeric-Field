from __future__ import division
import string
from Blob import Blob, Point, blobs_to_lsts
from mathparse import math_parse
from shapes import create_shape, return_var
## <expr> ->    <shape> | <declaration>
##
## <declaration> -> var(*variable-name,*number)
## 
## <shape> ->   rectangle (<arg>,<arg>,<arg>,<arg>,<arg>,<math>) | 
##              line(<arg>,<arg>,<arg>,<arg>,<arg>,<math>) |
##              point(<arg>,<arg>,<arg>)
## 
## <arg>  ->    *variable-name | *number | <math>
##
## <math> -> sin(<math>) | cos(<math>) | tan<math> | pow(<math>, arg) |


def parse_dsl(prog,gui_help_msg):

    ## Initialize lists for processing
    ## _out indicates that this will be returned to caller

    points = []
    blobs = []          ## Internal storage for 'blobs' of charge which are flattened
                        ## into output lists. Allows for groups of charges with the
                        ## same math expression to be calculated at once.

    xs_out = []         ## Output list for x locations of points
    ys_out = []         ## Output list for y locations of points
    cs_out = []         ## Output list for charges (calculated with math_parse)
    outs = (xs_out, ys_out, cs_out)

    '''Parse the domain language given a valid string. All atoms will be converted to
    python objects or functions. See top of file for CFG

    Params: 
            prog            -> string representing a program in the DSL
            gui_help_msg    -> callback to display help message on empty string'''

    if prog == 'help':      ## Display help message on gui if string is help, and exit
        gui_help_msg()
        return None


    def eval_args(args):
        '''Change string of args to list of args, looking up vars in the process'''
        out = []
        for arg in args:
            try: out.append(int(arg))
            except ValueError:
                try:
                    out.append(return_var(arg))
                except KeyError:
                    out.append(arg)        #declartion; proceed to function call 
        return out


    def parse(prog):
        '''Parse functions and their arguments'''

        for op,args in tokenize(prog):
            args = eval_args(args)
            create_shape(blobs,outs,op,*args)

    def tokenize(prog):
        ''' Tokenize a program'''
        out = []
        prog = prog.split('\n')
        for line in prog:
            parts = line.split('(')
            if parts != ['']:
                op = parts[0]
                args = parts[1][:-1].split(',')

                yield op,args



    parse(prog)
    blobs_to_lsts(blobs,outs)

    return xs_out, ys_out, cs_out
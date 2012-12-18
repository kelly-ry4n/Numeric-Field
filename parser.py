from __future__ import division
import string
from numpy import linspace
from mathparse import math_parse
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

class Point:

    def __init__(self,x,y, charge=1):
        self.x = x
        self.y = y
        self.charge = charge

class Blob:

    def __init__(self):
        self.xs = []
        self.ys = []
        self.charges = []
        self.math=lambda x,y : 1

    def __repr__(self):
        print "BLOB"
        for x,y in zip(self.xs, self.ys):
            print x, y
        return 'END BLOB'

    def add_point(self,pt):
        self.xs.append(pt.x)
        self.ys.append(pt.y)

    def apply_math(self):
        for x,y in zip(self.xs,self.ys):
            self.charges.append(self.math(x,y))
            #self.math(x, y)


def parse_dsl(prog,gui_help_msg):

    if prog == 'help':
        gui_help_msg()
        return None

    points = []
    blobs = []
    xs_out = []
    ys_out = []
    cs_out = []
    variables = {}

    def blobs_to_lsts(blobs):
        for blob in blobs:
            blob.apply_math()
            for x,y,c in zip(blob.xs,blob.ys,blob.charges):
                xs_out.append(x)
                ys_out.append(y)
                cs_out.append(c)



    def define_variable(name,value):
        variables[name] = value

    def point(x,y,charge=1):
        xs_out.append(x)
        ys_out.append(y)
        cs_out.append(charge)

    def rectangle(x0,y0,x1,y1,res,math):
        rect = Blob()

        xs = linspace(x0,x1, res/(y1-y0))
        ys = linspace(y0,y1, res/(x1-x0))
        f = math_parse(math)
        for x in xs:
            for y in ys:
                rect.add_point(Point(x,y))

        rect.math = lambda x, y: eval(f)

        blobs.append(rect)

    def line(x0,y0,x1,y1,res,math):
        lin = Blob()
        horizontal = linspace(x0,x1,res)
        m = (y1-y0)/(x1-x0)
        b = y0- m*x0
        f = math_parse(math)
        for x,y in zip(horizontal, (m*horizontal) + b):
            lin.add_point(Point(x,y))

        lin.math = lambda x, y: eval(f)

        blobs.append(lin)

    def return_var(var):
        if type(var) == type(int) or type(var) == type(float):
            return var
        return variables[var]

    def eval_args(args):
        out = []
        for arg in args:
            try: out.append(int(arg))
            except ValueError:
                try:
                    out.append(return_var(arg))
                except KeyError:
                    out.append(arg)        #declartion; proceed to function call 
        return out


    funcs = {
                'var'       : define_variable,
                'rectangle' : rectangle,
                'line'      : line,
                'point'     : point,
             }



    def parse(prog):

        for op,args in tokenize(prog):
            args = eval_args(args)
            funcs[op](*args)

    def tokenize(prog):
        out = []
        prog = prog.split('\n')
        for line in prog:
            parts = line.split('(')
            if parts != ['']:
                op = parts[0]
                args = parts[1][:-1].split(',')

                yield op,args


    parse(prog)
    blobs_to_lsts(blobs)
    print xs_out
    print ys_out
    print cs_out
    return xs_out, ys_out, cs_out
    


if __name__ == '__main__':
    test='rectangle[1,1,2,2,4, * + x 1 + x 2]\nrectangle[1,1,2,2,4, / + x 1 + x 2]'
    parse_dsl(test, lambda: None)
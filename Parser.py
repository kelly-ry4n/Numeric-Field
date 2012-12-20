from __future__ import division
import string
from numpy import linspace, sin, cos, tan, pi, exp, log, log10, radians
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
        '''A temperary container for points which should be flattened into a list or
        array.'''
        self.xs = []
        self.ys = []
        self.charges = []

        ## self.math is a function object which should be created and bound by parsing
        self.math=lambda x,y : 1
        self.x_parameters = lambda t: 1
        self.y_parameters = lambda t: 1

    def __repr__(self):
        '''Print points in self'''
        print "BLOB"
        for x,y in zip(self.xs, self.ys):
            print x, y
        return 'END BLOB'

    def add_point(self,pt):
        self.xs.append(pt.x)
        self.ys.append(pt.y)

    def apply_math(self):
        '''If a parsed math expression describes the charge of the particle at a point,
        this numerically adds this value to self.chares'''
        for x,y in zip(self.xs,self.ys):
            self.charges.append(self.math(x,y))
            #self.math(x, y)


def parse_dsl(prog,gui_help_msg):
    '''Parse the domain language given a valid string. All atoms will be converted to
    python objects or functions. See top of file for CFG

    Params: 
            prog            -> string representing a program in the DSL
            gui_help_msg    -> callback to display help message on empty string'''

    if prog == 'help':      ## Display help message on gui if string is help, and exit
        gui_help_msg()
        return None

    ## Initialize lists for processing
    ## _out indicates that this will be returned to caller

    points = []
    blobs = []          ## Internal storage for 'blobs' of charge which are flattened
                        ## into output lists. Allows for groups of charges with the
                        ## same math expression to be calculated at once.

    xs_out = []         ## Output list for x locations of points
    ys_out = []         ## Output list for y locations of points
    cs_out = []         ## Output list for charges (calculated with math_parse)
    variables = {}      ## A small namespace for any variables which are defined


    def blobs_to_lsts(blobs):
        ''' 'Flatten' the list of blobs to the three output lists, applying math
        as we go.'''

        for blob in blobs:
            blob.apply_math()       ## blob.apply_math is defined at runtime by
                                    ## parsing the last argument of a blob-creator
                                    ## like rectangle into a math expression of
                                    ## x and x

                                    ## TODO: add time dependance (t?)

            for x,y,c in zip(blob.xs,blob.ys,blob.charges):   ## Construct output lists
                xs_out.append(x)                                
                ys_out.append(y)
                cs_out.append(c)

            ## TODO: convert to numpy arrays... shouldn't cause too many problems..
            ##       .. I think



    def define_variable(name,value):
        '''Add variable <name> to the varaible namespace for this run'''
        variables[name] = value

    def point(x,y,charge=1):
        '''Not to be confused with the class Point. 

        Adds a point directly to the output lists, with default charge 1'''

        xs_out.append(float(x))            ## Append to the three lists
        ys_out.append(float(y))
        cs_out.append(float(charge))       ## Chage default arg with their argument
                                    ## of point in the parser's input string

    def rectangle(x0,y0,x1,y1,res,math):
        '''Create a rectangular blob of charge given coordinates which represent 
        diagonal corners.

        Params:
                res ->  Correlated with the 'resolution' of the rectangle. Larger
                        will lead to longer and finer calculations

                math -> Math is the string containing a Polish notation function
                        of X, Y (TODO: add T). It is parsed into a function
                        using mathparse.math_parse'''

        rect = Blob()                       ## Initialize a new Blob...

        xs = linspace(x0,x1, res/(y1-y0))   ## Set up a vertical and horizontal line
        ys = linspace(y0,y1, res/(x1-x0))   ## of charges

        for x in xs:                        ## Basically set up a meshgrid of x and y
            for y in ys:                    ## TODO: Look into replacing with Meshgrid.

                rect.add_point(Point(x,y))  ## Add each point to the blob

        f = math_parse(str(math))           ## Parse the Polish notation into python
                                            ## syntax.

        rect.math = lambda x, y: eval(f)    ## Evaluate the python syntax string
                                            ## into an expression, and bind it to
                                            ## a function at the math method of
                                            ## our blob

        blobs.append(rect)                  ## Put it on the list for later flattening


    def line(x0,y0,x1,y1,res,math):
        '''Create a linear blob given start and stop corridnates, a number of points
        on the line, and a math expression to be parsed by mathparse.math_parse.'''

        lin = Blob()                        ## Iniitialize a new blob

        horizontal = linspace(x0,x1,res)    ## Make a line along x

        m = (y1-y0)/(x1-x0)                 ## Map horizontal onto the line
        b = y0- m*(x1-x0)                   ## using y-mx + b

        for x,y in zip(horizontal, (m*horizontal) + b):
            lin.add_point(Point(x,y))


        f = math_parse(str(math))                ## Parse and assign math to blob.math()
        lin.math = lambda x, y: eval(f)

        blobs.append(lin)                   ## Put it on the list for later flattening

    def circle(x0,y0,radius,start_arc,end_arc,numpoints,math):
        """Create a circle of charge by using polar notation. Circle will have a start and stop end_arc
        given in degrees (for covinience)."""

        circle = Blob()                  ##Spiffy new blob

        theta = radians(linspace(start_arc,end_arc,numpoints)) #figure out our angles

        xs = radius*cos(theta)+x0                              #Build up our xs and ys
        ys = radius*sin(theta)+y0

        for x,y in zip(xs,ys):
            circle.add_point(Point(x,y))

        f = math_parse(str(math))                             #Parse some math for the charges
        circle.math = lambda x, y: eval(f)

        blobs.append(circle)                     #Stick into the main blob

    def parametric_curve(s1, s2, f1, f2, res, math):
        ''' Creates a blob which is a parametric curve of the form f(x,y) = (g(t),h(t))

        s1, s2 donate the domain of the parameter, fx is the x component, fy is the y compenent
        '''
        curve = Blob()                  #New blob

        domain = linspace(s1,s2,res)    # Domain of the parameterizing variable


        f1_func = lambda s: eval(math_parse(f1))  # We're gonna have a two part math here, in
        f2_func = lambda s: eval(math_parse(f2))  # addition to the usual to calculate x and y

        calc_charges = lambda x, y: eval (math_parse(str(math)))


        xs = f1_func(domain)
        ys = f2_func(domain)

        for x,y in zip(xs, ys):
            curve.add_point(Point(x,y))

        curve.math = calc_charges

        blobs.append(curve)


    def return_var(var):
        '''Looks up a variable or atom in the parse namespace'''

        ## If it's an int or float, it's an atom, and just return it.
        if type(var) == type(int) or type(var) == type(float):
            return var

        return variables[var]       ## Else, look up in parse namespace

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
            funcs[op](*args)

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

## map strings from DSL to their functions in the interpriter
    funcs = {
                'var'       : define_variable,
                'rectangle' : rectangle,
                'line'      : line,
                'point'     : point,
                'circle'    : circle,
                'curve'     : parametric_curve
             }

## run

    parse(prog)
    blobs_to_lsts(blobs)

    return xs_out, ys_out, cs_out
from Blob import Blob, Point
from numpy import linspace
from mathparse import math_parse
from numpy import linspace, sin, cos, tan, pi, exp, log, log10, radians

variables = {}

def define_variable(name,value):
    variables[name] = value

def return_var(var):
    '''Looks up a variable or atom in the parse namespace'''

    ## If it's an int or float, it's an atom, and just return it.
    if type(var) == type(int) or type(var) == type(float):
        return var
    return variables[var]


def create_shape(blobs,outs,name,*args):
    '''Gets blobs into the local namespace'''

    xs_out,ys_out,cs_out = outs[0],outs[1],outs[2]


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

    shapes = {
            'point'             :   point,
            'rectangle'         :   rectangle,
            'line'              :   line,
            'circle'            :   circle,
            'curve'             :   parametric_curve,
            'var'               :   define_variable
    }

    shapes[name](*args)
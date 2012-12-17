import string
from numpy import linspace
## <expr> ->    <shape> | <declaration>
##
## <declaration> -> var(*variable-name,*number)
## 
## <shape> ->   rectangle (<arg>,<arg>,<arg>,<arg>,<arg>) | line(<arg>,<arg>,<arg>,<arg>,<arg>) |
##              point(<arg>,<arg>)
## 
## <arg>  ->    *variable-name | *number

def parse_dsl(prog):

    points_x = []
    points_y = []
    variables = {}

    def define_variable(name,value):
        variables[name] = value

    def point(x,y):
        points_x.append(x)
        points_y.append(y)

    def rectangle(x0,y0,x1,y1,res):
        xs = linspace(x0,x1, res/(y1-y0))
        ys = linspace(y0,y1, res/(x1-x0))

        for x in xs:
            for y in ys:
                point(x,y)

    def line(x0,y0,x1,y1,res):
        horizontal = linspace(x0,x1,res)
        m = (y1-y0)/(x1-x0)
        b = y0- m*x0
        for x,y in zip(horizontal, (m*horizontal) + b):
            point(x,y)

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

    return points_x, points_y

print zip(points_x,points_y)
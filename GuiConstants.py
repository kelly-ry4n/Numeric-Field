

GUI_CONSTANTS = {}
    ## String for the default text for the text input box
GUI_CONSTANTS["default_input_text"] = \
'''curve(0,10,* 3 * cos s - 1 cos s,* 3 * sin s - 1 cos s ,20,  * -1 x)
point(3,0,5)'''

    ## Types of plots for plot choice dropdown

GUI_CONSTANTS["plot_type_choices"] =\
[
    'Contour Plot',
    'Vector Field',
    'Vector with Contour',
    '3d -- NOT IMPLIMENTED'
]

    ## Method of calculating W for second dropdown

GUI_CONSTANTS["vector_drawing_choices"] =\
 [
    'Magnitude',
    'Sum',
    'Multiply',
    'Vertical Divergence',
    'Horizontal Divergence',
    'Division Sum',
    'Dot'
]

    ## Options for field type dropdown
    ## TODO: Figure out quantum and einstien

GUI_CONSTANTS["field_type_choices"] =\
[
    'Gravitational',
    'Electric'
]

GUI_CONSTANTS["Cache"] =\
[ 0,0,0,0,0,0
    #Will contain, at runtime, a cache of the text boxes,
    #ie, domain, range, plot type, field type, command
]

GUI_CONSTANTS["Field_Cache"] =\
[0,0,0,0,0,0,0,0,0,0
    #Will contain the values needed to replot certain things without
    #needing to redo all the math
]

GUI_CONSTANTS['help_string'] = \
'''Statements:
var(<name>,number)                 -   Assigns number to <name>
point(x,y,c)                       -   Creates a point at x,y, with charge
line(x1,y2, x2,y2, numpoints, c)   -   Creates a line of points, each with charge c from (x1,y1) to (x2,y2)
rectangle(x1,y1,x2,y2,res, c)      -   Create a rectangle bounded by two corner points (x1,y1) and (x2,y2)\
where the charge density is related to res, and c gives the charge of the individual points
circle(x0,y0,radius,start_arc,end_arc,numpoints,c)  -Creates a part or a whole circle of charges, (x0,y0) is\
the center of the circle, the arcs are given in degrees.

Charges can be defined using Polish math notation ( + 1 1 is equivalent to 1+1)
Supported operations are: +, -, *, /, ^, sin, cos, tan, log, log10, exp
'''
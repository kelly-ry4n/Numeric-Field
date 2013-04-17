Numeric-Field
=============

Numeric approximations of physical field equations; Graphical results.

A quite demo/writeup at http://realitycoded.com/projects/numericfield.html

Requirements - Python 2.7, WXwidgits, Numpy to run from source.

Windows executable available at http://realitycoded.com/downloads/numeric-field.exe

Contact kelly.ry4n@gmail.com with any questions.

USAGE

Run DrawGui.py to start the program, or run the executable.

The top bar has three menues and one Load button. The first is used to select between plotting a contour map and a
vector field. The second determines which combination of the X and Y force vectors are used to construct the plot.
For example, Magnitude takes the magnitue of the sum of the vectors and is probably what you think of when you
think of a force plot. The last menu adjusts between gravitational and magnetic fields. The magnitues change,
and magnetic fields do not assume all charges to be postive (all masses are positive).

Below that is the render window, and options for the domain to plot. This only effects the plot domain, not the domain
over which values are calulated. In other words, if there are charges outside the plot domain, they will still
be used in the calculations.

Below that are the update and save buttons, and the input field.

Type help and then update to see the following:

Statements:
point(x,y,c)                       -   Creates a point at x,y, with charge

line(x1,y2, x2,y2, numpoints, c)   -   Creates a line of points, each with charge c from (x1,y1) to (x2,y2)

rectangle(x1,y1,x2,y2,res, c)      -   Create a rectangle bounded by two corner points (x1,y1) and (x2,y2)where the charge

density is related to res, and c gives the charge of the individual points

curve(start,stop,x_curve,y_curve ,num_points,field_expression) - creates a parametric curve with num_curve points
from start < s < stop and each component defined by x_curve and y_curve. The charge density is defined as a field
over the X and Y basis. For a constant field, simply enter a constant with no dependance on x or y.

Charges can be defined using Polish math notation ( + 1 1 is equivalent to 1+1)
Supported operations are: +, -, *, /, ^, sin, cos, tan, log, log10, exp


LISCENCE - This code and software is provided in hopes that it will be useful. Derivative works need not use
any specific liscence, nor cite this as an original source, although getting credit is always nice.

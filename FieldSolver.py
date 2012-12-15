from numpy import sqrt

def mag(x1,x2,y1,y2):
    return sqrt(  (x2-x1)**2. + (y2-y1)**2.  )

def force_x(x1,x2,y1,y2):
    x_comp = (x2-x1)/mag(x1,x2,y1,y2)/mag(x1,x2,y1,y2)
    return x_comp

def force_y(x1,x2,y1,y2):
    y_comp = (y2-y1)/mag(x1,x2,y1,y2)/mag(x1,x2,y1,y2)
    return y_comp

def test_force_x(x0,y0,xs,ys):
    return sum([force_x(x0,x1,y0,y1) for x1,y1 in zip(xs,ys)])

def test_force_y(x0,y0,xs,ys):
    return sum([force_y(x0,x1,y0,y1) for x1,y1 in zip(xs,ys)])

def U_f(X,Y):
    return -X/mag(X,0,Y,0)**2

def V_f(X,Y):
    return -Y/mag(X,0,Y,0)**2
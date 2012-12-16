from numpy import sqrt, linspace, meshgrid

def mag(x1,x2,y1,y2):
    return sqrt(  (x2-x1)**2. + (y2-y1)**2.  )

def force_x(x1,x2,y1,y2):
    return (x2-x1)/mag(x1,x2,y1,y2)**2

def force_y(x1,x2,y1,y2):
    return (y2-y1)/mag(x1,x2,y1,y2)**2

def test_force_x(x0,y0,xs,ys):
    return sum([force_x(x0,x1,y0,y1) for x1,y1 in zip(xs,ys)])

def test_force_y(x0,y0,xs,ys):
    return sum([force_y(x0,x1,y0,y1) for x1,y1 in zip(xs,ys)])

def U_f(X,Y):
    return -X/mag(X,0,Y,0)**2

def V_f(X,Y):
    return -Y/mag(X,0,Y,0)**2


def force_field(fig, plot_type, vector_type, xd, yr, res=0.1, xs, ys):
    x=linspace(xd[0],xd[1], res)
    y=linspace(yr[0], yr[1], res)
    xy=meshgrid(x,y)


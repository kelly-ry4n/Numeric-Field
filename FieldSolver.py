from numpy import sqrt, linspace, meshgrid
import PlotOnFig

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



def force_field(fig, plot_type, vector_type, xd, yr, res=100, xs, ys):
    """
    Function takes 'fig'(figure object) to plot to, the kind of 'plot_type' and vector_type',
    'xd' being a tuple with the domain of x, 'yr' being a tuple with the range of y,
    'res' as a float being the resolution in the x and y, and finally 'xs' and 'ys' as
    a list of arrays defining some blob
    """
    
    if plot_type=='Vector with Contour':
        ## Calculate both meshgrids for vectors and contours

        ## Set up a meshgrid for calculating contours
        X = linspace(xd[0],xd[1], res)
        Y = linspace(yr[0], yr[1], res)
        X, Y = meshgrid(X,Y)

        ## Set up a meshgrid for calculating vectors
        Xq = linspace(xd[0],xd[1], res/5)
        Yq = linspace(yr[0], yr[1], res/5)
        Xq, Yq = meshgrid(Xq,Yq)

        ## Evaluate the meshgrid at point (X,Y) for contours
        F_x = test_force_x(X,Y,xs,ys)
        F_y = test_force_y(X,Y,xs,ys)
     
        ## Evaluate the meshgrid at point (X,Y) for vectors
        F_xq = test_force_x(Xq,Yq,xs,ys)
        F_yq = test_force_y(Xq,Yq,xs,ys)

    if plot_type=='Contour Plot':
        ## Set up a meshgrid for calculating contours
        X = linspace(xd[0],xd[1], res)
        Y = linspace(yr[0], yr[1], res)
        X, Y = meshgrid(X,Y)

        ## Evaluate the meshgrid at point (X,Y) for contours
        F_x = test_force_x(X,Y,xs,ys)
        F_y = test_force_y(X,Y,xs,ys)

    if plot_type=='Vector Field':
        ## Set up a meshgrid for calculating vectors
        Xq = linspace(xd[0],xd[1], res/5)
        Yq = linspace(yr[0], yr[1], res/5)
        Xq, Yq = meshgrid(Xq,Yq)
        
        ## Evaluate the meshgrid at point (X,Y) for vectors
        F_xq = test_force_x(Xq,Yq,xs,ys)
        F_yq = test_force_y(Xq,Yq,xs,ys)



    ## Pass values to plot_on_fig
    plot_on_fig
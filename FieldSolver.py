from __future__ import division
from numpy import sqrt, linspace, meshgrid, array
from PlotOnFig import plot_on_fig

def mag(x1,x2,y1,y2):
    return sqrt(  (x2-x1)**2. + (y2-y1)**2.  )

def force_x(x1,x2,y1,y2):
    return (x2-x1)/mag(x1,x2,y1,y2)**3

def force_y(x1,x2,y1,y2):
    return (y2-y1)/mag(x1,x2,y1,y2)**3

def test_force_x(x0,y0,xs,ys):
    return sum([force_x(x0,x1,y0,y1) for x1,y1 in zip(xs,ys)])

def test_force_y(x0,y0,xs,ys):
    return sum([force_y(x0,x1,y0,y1) for x1,y1 in zip(xs,ys)])



def force_field(fig, plot_type, vector_type, xd, yr, xs, ys,
                 field_type, charge=-0.001, res=100):
    """
    Function takes '
    fig'(figure object) to plot to, the kind of 'plot_type' and vector_type',
    'xd' being a tuple with the domain of x, 'yr' being a tuple with the range of y,
    'res' as a float being the resolution in the x and y, and finally 'xs' and 'ys' as
    a list of arrays defining some blob.
    field_type is a string stating which calcuations to do (either Gravitational or Electric), charge is float
    dictating the overall charge of the blob (negative charges are abs() when using Gravitational)
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
        
        if field_type=='Gravitational':
            F_x = F_x*(6.67384e-11)*abs(charge)
            F_y = F_y*(6.67384e-11)*abs(charge)
            F_xq = F_xq*(6.67384e-11)*abs(charge)
            F_yq = F_yq*(6.67384e-11)*abs(charge)
        elif field_type=='Electric':
            F_x = F_x*(8.98755e9)*charge
            F_y = F_y*(8.98755e9)*charge
            F_xq = F_xq*(8.98755e9)*charge
            F_yq = F_yq*(8.98755e9)*charge

        F = (F_x,F_y)
        Fq = (F_xq,F_yq) 

        plot_on_fig(fig, X, Y, Xq, Yq, F, Fq, res, direc=vector_type)

    elif plot_type=='Contour Plot':
        ## Set up a meshgrid for calculating contours
        X = linspace(xd[0],xd[1], res)
        Y = linspace(yr[0], yr[1], res)
        X, Y = meshgrid(X,Y)

        ## Evaluate the meshgrid at point (X,Y) for contours
        F_x = test_force_x(X,Y,xs,ys)
        F_y = test_force_y(X,Y,xs,ys)
        
        if field_type=='Gravitational':
            F_x = F_x*(6.67384e-11)*abs(charge)
            F_y = F_y*(6.67384e-11)*abs(charge)
        elif field_type=='Electric':
            F_x = F_x*(8.98755e9)*charge
            F_y = F_y*(8.98755e9)*charge

        F = (F_x,F_y)

        plot_on_fig(fig, X, Y, None, None, F, None, res, direc=vector_type)

    elif plot_type=='Vector Field':
        ## Set up a meshgrid for calculating vectors
        Xq = linspace(xd[0],xd[1], res/5)
        Yq = linspace(yr[0], yr[1], res/5)
        Xq, Yq = meshgrid(Xq,Yq)
        
        ## Evaluate the meshgrid at point (X,Y) for vectors
        F_xq = test_force_x(Xq,Yq,xs,ys)
        F_yq = test_force_y(Xq,Yq,xs,ys)
        
        if field_type=='Gravitational':
            F_xq = F_xq*(6.67384e-11)*abs(charge)
            F_yq = F_yq*(6.67384e-11)*abs(charge)
        elif field_type=='Electric':
            F_xq = F_xq*(8.98755e9)*charge
            F_yq = F_yq*(8.98755e9)*charge

        Fq = (F_xq,F_yq)

        plot_on_fig(fig, None, None, Xq, Yq, None, Fq, res, direc=vector_type)
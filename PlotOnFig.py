from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
from numpy import sin, cos, abs, array, arange, meshgrid, divide, linspace, e, tan, dot
import matplotlib.mlab as mlab

def plot_on_fig(fig, Ustr, Vstr, progress_q, res, direc = 'sum'):

    ## Default plot parameters
    ## TODO: move to function kwargs
    x1,x2 = -5,5
    y1,y2 = -5,5
    res = res
    resq = 20
    dt = 0.01
    t = 0


    def U_f(X,Y):
        '''Using expression strings from the function call, calculate U(X,Y) for each element of
        the meshgrid'''

        ## TODO: Change to numpy computation.
        ## TODO: Get rid of eval()... parse expressions externally
        out = []
        count = 0
        for X, Y in zip(X, Y):
            count += 1
            progress_q.put(int(count*100/float(res)))

            out.append(eval(Ustr))
        return array(out)

    def V_f(X,Y):
        '''Using expression strings from the function call, calculate V(X,Y) for each element of
        the meshgrid'''

        ## TODO: Change to numpy computations
        ## TODO: Get rid of eval()... parse expressions externally
        out = []
        count = 0
        for X, Y in zip(X, Y):
            #print count
            count += 1
            progress_q.put(int(count*100/float(res)))

            out.append(eval(Vstr))
        return array(out)

    ## Varaibles ending with a little q indicate that the are used for plotting the quiver.
    ## This requires a much lower resolution than the contour, because too many arrows leads to
    ## a very cluttered look.

    ## Set up a meshgrid for plotting vectors
    Xq = linspace(x1, x2, resq)
    Yq = linspace(y1, y2, resq)
    Xq, Yq = meshgrid(Xq, Yq)

    ## Evaluate the meshgrid using the expressions for U and V which are passed to plot_on_fig
    Uq = U_f(Xq, Yq)
    Vq = V_f(Xq, Yq)

    ## Set up a meshgrid for plotting the contours.
    ## Plot resolution determined by caller.

    X = linspace(x1, x2, res)
    Y = linspace(y1, y2, res)
    X, Y = meshgrid(X, Y)

    ## Evaluate the meshgrid at X and Y for U and V
    U = U_f(X,Y)
    V = V_f(X,Y)

    ## TODO: Split the math and plotting into different modules

    ## A few methods of computing UV 'magnitudes' for plotting the contours
    plot_arrow_modes = {
                            'sum_mag'   : lambda: abs(U)+abs(V),
                            'sum'       : lambda: U+V          ,
                            'dot'       : lambda: dot(U,V)     ,
                            'mul'       : lambda: V*U          ,
                            'div_vert'  : lambda: V/U          ,
                            'div_hori'  : lambda: U/V          ,
                            'div_sum'   : lambda: V/U + U/V    ,
                        }

    W = plot_arrow_modes[direc]()

    ax = fig.add_subplot(111)
    ax.clear()

    ax.contourf(X,Y,W,100)
    ax.quiver(Xq,Yq,Uq,Vq, pivot='mid')

if __name__ == '__main__':
    import Queue

    fig = plt.figure()
    plot_on_fig(fig, 'cos(X)', 'sin(Y)',Queue.Queue(), 100, direc='sum')
    fig.show()
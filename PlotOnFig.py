import matplotlib.pyplot as plt
from numpy import abs, array, divide, dot

def plot_on_fig(fig, X, Y, Xq, Yq, F, Fq, res, direc = 'Sum'):
    """
    'fig'--> figure object, X and Y are components of meshgrid, Xq and Yq are
    components of the same meshgrid but at a fifth the resolution, 'F'--> 2-item tuple containing the
    force in the x and y directions respectively, 'Fq' similar to 'F' but once again at a fifth the 
    resolution, 'res' is oft mentioned resolution, and 'direc' --> string matching one of the dictionary
    keys in 'plot_arrow_modes' below.
    """

    if X is not None:
        U = F[0]
        V = F[1]
    
    if Xq is not None:
        Uq = Fq[0]
        Vq = Fq[1]
    
    ## A few methods of computing UV 'magnitudes' for plotting the contours
    plot_arrow_modes = {
                            'Magnitude'              : lambda: abs(U)+abs(V),
                            'Sum'                    : lambda: U+V          ,
                            'Dot'                    : lambda: dot(U,V)     ,
                            'Multiply'               : lambda: V*U          ,
                            'Vertical Divergence'    : lambda: V/U          ,
                            'Horizontal Divergence'  : lambda: U/V          ,
                            'Division Sum'           : lambda: V/U + U/V    ,
                        }

    ax = fig.add_subplot(111)
    ax.clear()


    if X is not None:
        W = plot_arrow_modes[direc]()
        ax.contourf(X,Y,W,res)
    if Xq is not None:
        ax.quiver(Xq,Yq,Uq,Vq, pivot='mid')
    

if __name__ == '__main__':
    import Queue

    fig = plt.figure()
    plot_on_fig(fig, 'cos(X)', 'sin(Y)',Queue.Queue(), 100, direc='sum')
    fig.show()
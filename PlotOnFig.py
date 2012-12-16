import matplotlib.pyplot as plt
from numpy import abs, array, divide, dot

def plot_on_fig(fig, X, Y, Xq, Yq, F_x, F_y, F_xq, F_yq, res, direc = 'Sum'):

    U = F_x
    V = F_y
    Uq = F_xq
    Vq = F_yq
    
    ## A few methods of computing UV 'magnitudes' for plotting the contours
    plot_arrow_modes = {
                            'sum_mag'   : lambda: abs(U)+abs(V),
                            'Sum'       : lambda: U+V          ,
                            'dot'       : lambda: dot(U,V)     ,
                            'mul'       : lambda: V*U          ,
                            'div_vert'  : lambda: V/U          ,
                            'div_hori'  : lambda: U/V          ,
                            'div_sum'   : lambda: V/U + U/V    ,
                        }

    ax = fig.add_subplot(111)
    ax.clear()

    try:
        W = plot_arrow_modes[direc]()
    except TypeError:
        pass

    if X is not None:
        ax.contourf(X,Y,W,res)
    if Xq is not None:
        ax.quiver(Xq,Yq,Uq,Vq, pivot='mid')
    

if __name__ == '__main__':
    import Queue

    fig = plt.figure()
    plot_on_fig(fig, 'cos(X)', 'sin(Y)',Queue.Queue(), 100, direc='sum')
    fig.show()
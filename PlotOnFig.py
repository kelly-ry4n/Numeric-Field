from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
from numpy import sin, cos, abs, array, arange, meshgrid, divide, linspace, e, tan, dot
import matplotlib.mlab as mlab

def plot_on_fig(fig, Ustr, Vstr, progress_q, res, direc = 'sum'):

    ## Keep these above definitions
    x1,x2 = -5,5
    y1,y2 = -5,5
    res = res
    resq = 20
    dt = 0.01
    t = 0


    def U_f(X,Y):
        out = []
        count = 0
        for X, Y in zip(X, Y):
            count += 1
            progress_q.put(int(count*100/float(res)))

            out.append(eval(Ustr))
        return array(out)

    def V_f(X,Y):
        out = []
        count = 0
        for X, Y in zip(X, Y):
            #print count
            count += 1
            progress_q.put(int(count*100/float(res)))

            out.append(eval(Vstr))
        return array(out)

    #arrows, less

    Xq = linspace(x1, x2, resq)
    Yq = linspace(y1, y2, resq)
    Xq, Yq = meshgrid(Xq, Yq)

    Uq = U_f(Xq, Yq)
    Vq = V_f(Xq, Yq)

    ## contour, smoother

    X = linspace(x1, x2, res)
    Y = linspace(y1, y2, res)
    X, Y = meshgrid(X, Y)


    U = U_f(X,Y)
    V = V_f(X,Y)

    if direc == 'sum_mag':
        W = abs(U)+abs(V)
    elif direc == 'sum':
        W = U + V
    elif direc == 'dot':
        W = dot(U,V)
    elif direc == 'mul':
        W = U*V
    elif direc == 'div_vertical':
        W = V/U
    elif direc == 'div_horizontal':
        W = U/V
    elif direc == 'div_sum':
        W = V/U + U/V

    # plt.autoscale(enable=True, axis='both')
    # plt.grid('on')

    ax = fig.add_subplot(111)
    ax.clear()

    ax.contourf(X,Y,W,1000)
    #plt.contour(X,Y,W,10, linewidths=5)
    ax.quiver(Xq,Yq,Uq,Vq, pivot='mid')
    #plt.show()

if __name__ == '__main__':



    fig = plt.figure()#figsize=(23.5,13))

    plot_on_fig(fig, 'cos(X)', 'sin(Y)', direc='sum')
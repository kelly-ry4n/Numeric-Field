from __future__ import division
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
from numpy import sin, cos, abs, array, arange, meshgrid, divide,\
arccos, linspace, e, tan, dot, arcsin, sqrt, zeros, ones
import matplotlib.mlab as mlab

def plot_on_fig(fig, force_x,force_y, blob_x,blob_ys,blob_m=[], direc = 'sum_mag'):

    x1,x2 = -10,10
    y1,y2 = -10,10
    res = 100
    resq = 25
    dt = 0.01
    t = 0


    #arrows, less

    Xq = linspace(x1, x2, resq)
    Yq = linspace(y1, y2, resq)
    Xq, Yq = meshgrid(Xq, Yq)

    Uq = sum([test_force_x(Xq,Yq,blob_x,blob_y) for blob_y in blob_ys])
    Vq = sum([test_force_y(Xq,Yq,blob_x,blob_y) for blob_y in blob_ys])

    # Uq = test_force_x(Xq,Yq,blob_x,blob_y)
    # Vq = test_force_y(Xq,Yq,blob_x,blob_y)


    ## contour, smoother

    X = linspace(x1, x2, res)
    Y = linspace(y1, y2, res)
    X, Y = meshgrid(X, Y)


    U = sum([test_force_x(X,Y,blob_x,blob_y) for blob_y in blob_ys])
    V = sum([test_force_y(X,Y,blob_x,blob_y) for blob_y in blob_ys])
    #V = test_force_y(X,Y,blob_x,blob_y)

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
    plt.grid('on')

    #plt.contourf(X,Y,W,res)
    plt.contour(X,Y,W,400, linewidths=2)
    plt.quiver(Xq,Yq,Uq,Vq, pivot='mid')
    plt.show()

if __name__ == '__main__':

    for i in xrange(300):
        print '%s / %s' % (i, 300)
        n = 0

        def progress_bar(curr,tot):
            percent = int(curr*100/tot)
            print '[' + '='*percent + ' '*(100-percent) + ']'
            if percent == 100:
                print 'Rendering Plot...'

        def mag(x1,x2,y1,y2):
            return sqrt((x2-x1)**2+(y2-y1)**2.)

        def test_force_x(x0,y0,xs,ys):
            return sum([force_x(x0,x1,y0,y1) for x1,y1 in zip(xs,ys)])

        def test_force_y(x0,y0,xs,ys):
            return sum([force_y(x0,x1,y0,y1) for x1,y1 in zip(xs,ys)])

        def force_x(x1,x2,y1,y2):
            global n
            n += 1
            if n%100 == 0:
                progress_bar(n,1000)
            x_comp = cos(  arccos((x2-x1)/mag(x1,x2,y1,y2))  )/mag(x1,x2,y1,y2)
            return x_comp

        def force_y(x1,x2,y1,y2):
            y_comp = sin(  arcsin((y2-y1)/mag(x1,x2,y1,y2))  )/mag(x1,x2,y1,y2)
            return y_comp

        def U_f(X,Y):
            return -cos(arccos(X/sqrt(X**2+Y**2.)))/(X**2.+Y**2)

        def V_f(X,Y):
            return -sin(arcsin(Y/sqrt(X**2+Y**2.)))/(X**2+Y**2.)

        num_particles = 500
        blob_x = linspace(-10,10,num_particles)

        y1 = linspace(-3,-3,10)
        y2 = linspace(-3,-3,10)

        blob_ys = [sin(blob_x)]

        #blob_ys = [[i for q in xrange(-5,5)] for i in xrange(-5,5)]
        #blob_ys = [ones(num_particles) for i in linspace(-2,-2,num_particles)]

        # for i in blob_ys:
        #     print i
        #blob_y1 = blob_x ** 2
        # blob_y2 = blob_x ** 3


        fig = plt.figure(figsize=(23.5,13))

        plot_on_fig(fig, test_force_x,test_force_y,blob_x,blob_ys, direc='sum_mag')

from numpy import arange, sin, pi
from Queue import Queue
from threading import Thread

import matplotlib
matplotlib.use('WXAgg')     # matplotlib magic... I don't know what this does but I'm
                            # scared to remove it

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

from PlotOnFig import plot_on_fig

import wx

class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        self.parent = parent
        self.parent.SetSize((1000,1000))
        wx.Panel.__init__(self, parent)
        self.progress_q = Queue()

        self.vertical_sizer = wx.BoxSizer(wx.VERTICAL) # Our main sizer

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)

        self.vertical_sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.vertical_sizer.Add((0,10))

        self.U_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.U_input_text = wx.StaticText(self,label="Enter a function for U here:")
        self.U_input_field= wx.TextCtrl(self)
        self.U_input_field.ChangeValue('cos(X) + Y')

        self.U_horizontal_sizer.Add(self.U_input_text)
        self.U_horizontal_sizer.Add(self.U_input_field)
        self.U_horizontal_sizer.Add((10,0))

        self.vertical_sizer.Add(self.U_horizontal_sizer)
        self.vertical_sizer.Add((0,10))

        self.V_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.V_input_text = wx.StaticText(self,label="Enter a function for V here:")
        self.V_input_field= wx.TextCtrl(self)
        self.V_input_field.ChangeValue('sin(Y)')
        self.V_horizontal_sizer.Add(self.V_input_text)
        self.V_horizontal_sizer.Add(self.V_input_field)

        self.vertical_sizer.Add(self.V_horizontal_sizer)
        self.vertical_sizer.Add((0,10))

        self.update_fig_button = wx.Button(self, label='Update Figure')
        self.update_fig_button.Bind(wx.EVT_BUTTON, self.update_fig_from_button)

        self.progress_gauge = wx.Gauge(self,wx.GA_HORIZONTAL|wx.EXPAND|wx.GROW,range=100)
        self.status_text = wx.StaticText(self,wx.RIGHT,label="Render Complete")

        self.bottom_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bottom_horizontal_sizer.Add(self.update_fig_button)
        self.bottom_horizontal_sizer.Add((10,0))
        self.bottom_horizontal_sizer.Add(self.progress_gauge)
        self.bottom_horizontal_sizer.Add((10,0))
        self.bottom_horizontal_sizer.Add(self.status_text)
        self.vertical_sizer.Add(self.bottom_horizontal_sizer)

        self.SetSizer(self.vertical_sizer)
        self.Fit()

    def update_fig(self):

        plot_on_fig(self.figure, 'cos(X)', 'Y', self.progress_q, 100, direc='sum')

    def update_fig_from_button(self, e):
        t1 = Thread(target = self.threaded_progress_bar_update)
        t1.run()
        t2 = Thread(target = self.start_fig_update)
        t2.run()

    def start_fig_update(self):

        self.status_text.SetLabel('Computing Field...')

        Ustr = self.U_input_field.GetValue()
        Vstr = self.U_input_field.GetValue()
        plot_on_fig(self.figure, Ustr, Vstr, self.progress_q, 100, direc='sum')

        self.canvas.draw()
        self.status_text.SetLabel('Render Finished')

    def threaded_progress_bar_update(self):
        while 1:
            percent = self.progress_q.get()
            self.progress_gauge.SetValue(percent)
            if percent >= 100:
                break

        #self.update()



if __name__ == "__main__":

    def U_f(X,Y):
        from numpy import cos, sin
        return sin(X)

    def V_f(X,Y):
        from numpy import cos, sin
        return cos(Y)

    app = wx.PySimpleApp()
    fr = wx.Frame(None, title='test')
    panel = CanvasPanel(fr)
    panel.update_fig()
    fr.Show()
    app.MainLoop()
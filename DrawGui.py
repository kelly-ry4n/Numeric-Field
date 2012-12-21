from numpy import arange, sin, pi
from Queue import Queue
import os, array, sys, traceback

import matplotlib
matplotlib.use('WXAgg')     # matplotlib magic... I don't know what this does but I'm
                            # scared to remove it

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

import wx

class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        ''' The gui will be organized into one vertical sizing box, and several horizontal ones. The
        figure will be at the top, followed by space for user input and feedback'''
        self.parent = parent
        self.parent.SetSize((640,600))
        wx.Panel.__init__(self, parent)
        self.init_methods()
        self.init_ui()

    def init_methods(self):


        ############################## WARNING -- META ###################################
        ##                                                                              ##
        ## For each method of GuiMethods, bind the method to self using the method      ##
        ## name as self.                                                                ##
        ##                                                                              ##
        #################################################################################

        import GuiMethods as methods
        from types import MethodType
        for m in dir(methods):
            method = getattr(methods, m)
            if type(method) == type(lambda x: None):

                name = method.__name__
                exec 'self.%s = MethodType(method, self)' % (name) in locals()

    def init_ui(self):
        from GuiConstants import GUI_CONSTANTS

        self.helpstr            = GUI_CONSTANTS['help_string']
        default_input_text      = GUI_CONSTANTS['default_input_text']
        plot_type_choices       = GUI_CONSTANTS['plot_type_choices']
        vector_drawing_choices  = GUI_CONSTANTS['vector_drawing_choices']
        field_type_choices      = GUI_CONSTANTS['field_type_choices']


        self.vertical_sizer = wx.BoxSizer(wx.VERTICAL) # Our main sizer

        ## Set up the three dropdown boxes for selecting 
        ## what to plot and how it should look

        self.plot_type_selector = wx.ComboBox(  parent=self,
                                                choices=plot_type_choices,
                                                style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.plot_type_selector.SetValue('Contour Plot')

        self.vector_drawing_selector = wx.ComboBox(parent=self,
                                                   choices=vector_drawing_choices,
                                                   style = wx.CB_DROPDOWN|wx.CB_READONLY)
        self.vector_drawing_selector.SetValue('Magnitude')

        self.field_type_selector = wx.ComboBox(  parent=self,
                                                 choices= field_type_choices,
                                                 style = wx.CB_DROPDOWN|wx.CB_READONLY)
        self.field_type_selector.SetValue('Gravitational')

        self.dropdown_sizer = wx.BoxSizer(wx.HORIZONTAL)

        ## Load button

        self.load_charge_button = wx.Button(self,label='Load')
        self.save_charge_button = wx.Button(self,label='Save')
        #self.load_charge_button.SetSize((30,30))
        self.load_charge_button.Bind(wx.EVT_BUTTON, self.load_charge_field)
        self.save_charge_button.Bind(wx.EVT_BUTTON, self.save_charge_field)

        ## Put dropdown boxes and load button into horizontal sizer

        self.dropdown_sizer.Add(self.plot_type_selector)
        self.dropdown_sizer.Add(self.vector_drawing_selector)
        self.dropdown_sizer.Add(self.field_type_selector)
        self.dropdown_sizer.Add(self.load_charge_button)
        self.dropdown_sizer.Add(self.save_charge_button)

        self.vertical_sizer.Add(self.dropdown_sizer)

        ## Put horizontal sizer into vertical sizer

        self.vertical_sizer.Add((0,3))

        ## Setup a matplotlib figure for mutation by plot_on_fig

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)

        self.vertical_sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.vertical_sizer.Add((0,10))

        ## Set up text and domain inputs, add them to sizers

        self.x_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.x_input_text = wx.StaticText(self,label="Plot Domain: (x1, x2):")
        self.x1_input_field= wx.TextCtrl(self)
        self.x2_input_field= wx.TextCtrl(self)

        self.x1_input_field.ChangeValue('-5')
        self.x2_input_field.ChangeValue('5')

        self.x_horizontal_sizer.Add(self.x_input_text)
        self.x_horizontal_sizer.Add(self.x1_input_field)
        self.x_horizontal_sizer.Add(self.x2_input_field)
        self.x_horizontal_sizer.Add((10,0))

        self.vertical_sizer.Add(self.x_horizontal_sizer)
        self.vertical_sizer.Add((0,10))

        self.y_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.y_input_text = wx.StaticText(self,label="Plot Range (y1,y2):    ")

        self.y2_input_field = wx.TextCtrl(self)
        self.y1_input_field = wx.TextCtrl(self)

        self.y1_input_field.ChangeValue('-5')
        self.y2_input_field.ChangeValue('5')

        self.y_horizontal_sizer.Add(self.y_input_text)
        self.y_horizontal_sizer.Add(self.y1_input_field)
        self.y_horizontal_sizer.Add(self.y2_input_field)

        self.vertical_sizer.Add(self.y_horizontal_sizer)
        self.vertical_sizer.Add((0,10))

        self.update_fig_button  = wx.Button(self, label='Update Figure')
        self.save_fig_button    = wx.Button(self, label='Save Figure')
        self.update_fig_button.Bind(wx.EVT_BUTTON, self.update_fig_from_button)
        self.save_fig_button.Bind(wx.EVT_BUTTON, self.save_figure)

        self.progress_gauge = wx.Gauge(self,wx.GA_HORIZONTAL|wx.EXPAND|wx.GROW,range=100)
        self.status_text = wx.StaticText(self,wx.RIGHT,label="Render Complete")

        self.bottom_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bottom_horizontal_sizer.Add(self.update_fig_button)
        self.bottom_horizontal_sizer.Add(self.save_fig_button)
        self.bottom_horizontal_sizer.Add((10,0))
        self.bottom_horizontal_sizer.Add(self.progress_gauge)
        self.bottom_horizontal_sizer.Add((10,0))
        self.bottom_horizontal_sizer.Add(self.status_text)
        self.vertical_sizer.Add(self.bottom_horizontal_sizer)

        ## Input and output consoles

        self.output_text_ctrl= wx.TextCtrl(self,style = wx.TE_MULTILINE|wx.TE_READONLY,
                                            size = (620,75))
        self.output_text_ctrl.ChangeValue('Console..')
        self.input_text_ctrl = wx.TextCtrl(self,style = wx.TE_MULTILINE, size = (620,100))
        self.input_text_ctrl.ChangeValue(default_input_text)
        self.vertical_sizer.Add(self.input_text_ctrl)
        self.vertical_sizer.Add(self.output_text_ctrl)
        self.vertical_sizer.Add((0,10))

        self.SetSizer(self.vertical_sizer)
        self.Fit()

        


if __name__ == "__main__":

    try:
        app = wx.PySimpleApp()
        fr = wx.Frame(None, title='Field Plot')
        panel = CanvasPanel(fr)
        panel.update_fig()
        fr.Show()
        app.MainLoop()

    except Exception as Exc:
        ## Don't close till we see the error
        print '\n\n\n'
        traceback.print_exc(file=sys.stdout)
        raw_input('\n\n\nPress any key to continue')
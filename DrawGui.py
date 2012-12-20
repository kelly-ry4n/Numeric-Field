from numpy import arange, sin, pi
from Queue import Queue
from threading import Thread
import os, array, sys, traceback

import matplotlib
matplotlib.use('WXAgg')     # matplotlib magic... I don't know what this does but I'm
                            # scared to remove it

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

from FieldSolver import force_field
from PlotOnFig import plot_on_fig
from Parser import parse_dsl
from Files import get_data, save_data

import wx

class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        ''' The gui will be organized into one vertical sizing box, and several horizontal ones. The
        figure will be at the top, followed by space for user input and feedback'''
        self.parent = parent
        self.parent.SetSize((640,600))
        wx.Panel.__init__(self, parent)

## String for the default text for the text input box
        default_input_text = \
'''curve(0,10,* 3 * cos s - 1 cos s,* 3 * sin s - 1 cos s ,200,  * -1 x)
point(3,0,5)'''

## Types of plots for plot choice dropdown

        plot_type_choices = [
                                'Contour Plot',
                                'Vector Field',
                                'Vector with Contour',
                                '3d -- NOT IMPLIMENTED',
                            ]

## Method of calculating W for second dropdown

        vector_drawing_choices = [
                                    'Magnitude',
                                    'Sum',
                                    'Multiply',
                                    'Vertical Divergence',
                                    'Horizontal Divergence',
                                    'Division Sum',
                                    'Dot'
                                    ]


## Options for field type dropdown
## TODO: Figure out quantum and einstien

        field_type_choices = [
                                'Gravitational',
                                'Electric'
        ]



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

    def display_help_msg_callback(self):
        ''' Displays the help message in the output box'''
        helpstr = \
'''Statements:
var(<name>,number)                 -   Assigns number to <name>
point(x,y,c)                       -   Creates a point at x,y, with charge
line(x1,y2, x2,y2, numpoints, c)   -   Creates a line of points, each with charge c from (x1,y1) to (x2,y2)
rectangle(x1,y1,x2,y2,res, c)      -   Create a rectangle bounded by two corner points (x1,y1) and (x2,y2)\
 where the charge density is related to res, and c gives the charge of the individual points
circle(x0,y0,radius,start_arc,end_arc,numpoints,c)  -Creates a part or a whole circle of charges, (x0,y0) is\
the center of the circle, the arcs are given in degrees.

Charges can be defined using Polish math notation ( + 1 1 is equivalent to 1+1)
Supported operations are: +, -, *, /, ^, sin, cos, tan, log, log10, exp
 '''
        self.set_console_msg(helpstr)

    def set_console_msg(self,msg):
        '''Sets the output box text'''
        self.output_text_ctrl.ChangeValue(msg)

    def update_fig(self):
        '''Sends the figure to some math and plotting, comes back with a new image'''

        self.start_fig_update()


    def update_fig_from_button(self, e):
        '''Spawns threads for math and progress bar so that the gui doesn't die'''

        self.figure.clf()
        t = Thread(target = self.start_fig_update)
        t.run()

    def start_fig_update(self):
        '''Mutates the matplotlib figure to show data. Takes data from 
        various input fields.'''

        self.status_text.SetLabel('Computing Field...')

        domain_x = (float(self.x1_input_field.GetValue()),float(self.x2_input_field.GetValue()))
        range_y = (float(self.y1_input_field.GetValue()),float(self.y2_input_field.GetValue()))
        plot_type= self.plot_type_selector.GetValue()
        vector_type = self.vector_drawing_selector.GetValue()
        field_type = self.field_type_selector.GetValue()

        xs, ys, cs = parse_dsl(self.input_text_ctrl.GetValue(),self.display_help_msg_callback)

        if xs == []:
            self.set_console_msg('Input cannot be empty!\
                                 Update with "help" for commands')

        elif xs == None:
            pass

        else:

            force_field(self.figure, plot_type, vector_type,
                        domain_x, range_y,xs,ys,cs,field_type, res = 100)

            self.canvas.draw()
            self.status_text.SetLabel('Render Finished')

    def threaded_progress_bar_update(self):
        ''' Currently not in use'''
        while 1:
            percent = self.progress_q.get()
            self.progress_gauge.SetValue(percent)
            if percent >= 100:
                break

    def load_charge_field(self,e):
        ''' Load button functionality.'''
        wildcard = "Files (*.*)|*.*"
        open_dlg = wx.FileDialog(
            self, message = 'Choose file',
            defaultDir=os.getcwd()+"/Saves",
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR
            )

        if open_dlg.ShowModal() == wx.ID_OK:
            path = open_dlg.GetPaths()[0]

        xs,ys,cs = get_data(path)
        
        ## Build a command for the Gui and pass it along
        f=zip(xs,ys,cs)
        m=''
        for i in range(len(f)):
            s='point('
            for j in range(3):
                s= s+f[i][j]+','
            m= m+s[0:-1]+")\n"

        self.input_text_ctrl.ChangeValue(m)
        self.start_fig_update()
            
        open_dlg.Destroy()

    def save_charge_field(self,e):
        ''' Saves what's currently in the input box'''
        wildcard = "Files (*.*)|*.*"
        save_dlg = wx.FileDialog(
            self, message = 'Choose file',
            defaultDir=os.getcwd()+"/Saves",
            defaultFile="",
            wildcard=wildcard,
            style=wx.SAVE | wx.CHANGE_DIR
            )

        if save_dlg.ShowModal() == wx.ID_OK:
            path = save_dlg.GetPaths()[0]            
        save_dlg.Destroy()

        xs, ys, cs = parse_dsl(self.input_text_ctrl.GetValue(),
                                self.display_help_msg_callback)
        save_data(path,xs,ys,cs)
        


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
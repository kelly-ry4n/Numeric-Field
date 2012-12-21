from Files import get_data, save_data

from FieldSolver import force_field
from PlotOnFig import plot_on_fig
from Parser import parse_dsl
from threading import Thread

def display_help_msg_callback(self):
    ''' Displays the help message in the output box'''
    self.set_console_msg(self.helpstr)

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
    wildcard = "Files (*.figsave)|*.figsave"
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
    wildcard = "Files (*.figsave)|*.figsave"
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

def save_figure(self,e):
    wildcard = "PNG Image (*.png)|*.png"
    save_dlg = wx.FileDialog(
        self, message = 'Choose file',
        defaultDir=os.getcwd()+"/Saves",
        defaultFile="",
        wildcard=wildcard,
        style=wx.SAVE | wx.CHANGE_DIR
        )
    if save_dlg.ShowModal() == wx.ID_OK:
        filename = save_dlg.GetPaths()[0]            
    save_dlg.Destroy()
    self.figure.savefig(filename)
from parameters.plotting import Plot
from src.simulation import Simulation
import threading, time

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib, numpy as np
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import PySimpleGUI as sg

def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg
    
class MainThread(threading.Thread):
    def __init__(self, envrule, cellrule, *args, **kwargs):
        super(MainThread, self).__init__(*args, **kwargs)
        self.__flag = threading.Event() # The flag used to pause the thread
        self.__flag.set() # Set to True
        self.__running = threading.Event() # Used to stop the thread identification
        self.__running.set() # Set running to True
        self.daemon = True
        self.sim = Simulation(envrule, cellrule)
        self.sg_init()
        self.plot_stgs = Plot()
        
    def sg_init(self):
        sg.theme('SystemDefault1')
        self.font = ('Helvetica', 12)
        self.titlefont = ('Helvetica', 14, "bold")
        self.figsize = (20, 20)
        self.fig = None
        menu_layout = [
            ["Simulation", ["Next", "Launch"]],
            ["Edit Simulation", ["Parameters", "Environment Rule", "Cells Rule"]],
            ["Settings", ["Plotting", "Defaults"]],
        ]
        
        layout = [
            [sg.MenuBar(menu_layout)],
            [sg.Canvas(size=(16,16), key='plot')],
        ]
        
        self.window = sg.Window("Cell simulation", layout, font=self.font, resizable=True, finalize=True, location=(0, 0))
        self.window.bind('<Right>', 'right')

    def sg_plot(self):
        if self.fig:
            plt.clf()
            self.fig.get_tk_widget().forget()
            
        if self.sim.env.grid is None:
            self.fig = matplotlib.figure.Figure(figsize=self.figsize)
            self.fig.add_subplot(111)
            return self.fig
        
        plt.title(f"Epoch {self.sim.env.clock}")
        plt.imshow(self.sim.env.get_grid(self.plot_stgs.colors.copy()), interpolation="none", cmap="gist_ncar", vmin=0, vmax=len(self.plot_stgs.colors.copy()))
        return plt.gcf()
    
    def sg_change_params(self):
        pass
    
    def run(self):
        self.bool_resume = True  
        while self.__running.isSet():
            self.__flag.wait()
            self.fig = draw_figure(self.window['plot'].TKCanvas, self.sg_plot())
            self.sim.next()
            time.sleep(1/min(self.plot_stgs.fps, 30))

    def run_once(self):
        self.fig = draw_figure(self.window['plot'].TKCanvas, self.sg_plot())
        self.sim.next()

    def pause(self):
        self.__flag.clear()
        self.__running.wait()
        self.bool_resume = True
    
    def resume(self):
        self.__flag.set()
        self.__running.set()
        self.bool_resume = False

    def stop(self):
        self.__flag.set()
        self.__running.clear()

        
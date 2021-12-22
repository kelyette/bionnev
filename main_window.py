import tkinter as tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from parameters import plot_rules
from src.simulation import Simulation
from options_window import Settings

from inspect import getmembers, isfunction, isclass
import pickle
import os

class Gui:
    def __init__(self, default_envrule, default_cellrule, default_plotrule):
        self.sim = Simulation(default_envrule, default_cellrule)
        self.plot_stgs = getattr(plot_rules, default_plotrule)()
        self.init_window()

    def init_window(self):
        self.root = tk.Tk()
        self.root.title("Cell Simulation")
        self.frm_left = tk.Frame()
        self.frm_right = tk.Frame()

        
        self.lbl_stats = []
        for i,stat in enumerate(list(self.plot_stgs.stats.keys())):
            self.lbl_stats.append(tk.Label(text=f"{stat}: /", master=self.frm_left))
            self.lbl_stats[i].pack(side=tk.TOP, anchor=tk.NW)

        self.fig = Figure()
        self.init_plot()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frm_right)
        
        self.btn_launch = tk.Button(text='Launch', command=self.launch, master=self.frm_left)
        self.btn_pause = tk.Button(text='Pause',command=self.pause, master=self.frm_left)
        self.btn_settings = tk.Button(text='Settings',command=self.settings, master=self.frm_left)
        #self.btn_save = tk.Button(text='Save',command=self.save_state, master=self.frm_right)
        self.btn_next = tk.Button(text='Next', master=self.frm_left)
        
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.btn_settings.pack(side=tk.LEFT, anchor=tk.S)
        self.btn_pause.pack(side=tk.LEFT, anchor=tk.S)
        self.btn_launch.pack(side=tk.LEFT, anchor=tk.S)
        #self.btn_save.pack(side=tk.RIGHT, anchor=tk.S)
        self.frm_left.pack(side=tk.LEFT, anchor=tk.NW)
        self.frm_right.pack(side=tk.RIGHT, anchor=tk.NW)

    def init_plot(self):
        self.ax = self.fig.add_subplot(111)
        self.frame = self.ax.imshow(self.sim.env.get_grid(self.plot_stgs), interpolation="none", cmap="gist_ncar", animated=True)
        self.ax.set_xticks([])
        self.ax.set_yticks([])

    def updatefig(self, i):
        if (not i % self.plot_stgs.show_n) and (not self.paused):
            self.sim.next()
            self.update_stats()
        self.frame.set_array(self.sim.env.get_grid(self.plot_stgs))
        return self.frame, 
    
    def update_stats(self):
        for i, stat in enumerate(list(self.plot_stgs.stats.keys())):
            self.lbl_stats[i].config(text=f"{stat}: {self.plot_stgs.stats[stat](self.sim.env):0.{self.plot_stgs.stats_pres}f}")

    def start(self):
        self.started = True
        self.launched = False
        self.paused = False
        self.root.mainloop() 
        
    def launch(self):
        self.launched ^= True
        if self.launched:
            if self.started:
                self.canvas.draw_idle()
                self.ani = animation.FuncAnimation(self.fig, self.updatefig, interval=self.plot_stgs.fps, blit=False, repeat=True)
            self.btn_launch.config(text='Reset')
            self.ani.resume()  
        else: 
            self.sim.restart()
            self.btn_pause.config(text='Pause')
            self.btn_launch.config(text='Launch')
            self.paused ^= True
            self.ani.pause()
            
            
    def pause(self):
        self.paused ^= True
        button_txt = 'Resume' if self.paused else 'Pause'
        self.btn_pause.config(text=button_txt)
    
    def settings(self):
        set = Settings(self.sim, self.plot_stgs)
        set.start()
        
    def save_state(self, filename, folder='saves'):
        if filename in os.listdir(folder): 
            raise NameError('Save "{filename}" already exists.')
        
        with open(f'./{folder}/{filename}.pkl', 'a') as sf:
            pickle.dump(self.sim.copy(), sf)
        
    def load_state(self, filename, folder='saves'):
        if filename not in os.listdir(folder): 
            raise NameError('Save "{filename}" doesn\'t exist.')
        
        
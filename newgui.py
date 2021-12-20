import yaml
import tkinter as tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from parameters import plot_rules
from src.simulation import Simulation

with open("parameters/config.yaml", "r") as f:
    config = yaml.safe_load(f)
    
default_envrule = config["default_envrule"]
default_cellrule = config["default_cellrule"]
default_plotrule = config["default_plotrule"]

class GUI:
    def __init__(self, default_envrule, default_cellrule, default_plotrule):
        self.sim = Simulation(default_envrule, default_cellrule)
        self.plot_stgs = getattr(plot_rules, default_plotrule)()
        self.init_window()

    def init_window(self):
        self.root = tk.Tk()
        self.root.title("Cell Simulation")
        self.frm_top = tk.Frame()
        self.frm_stats = tk.Frame(master=self.frm_top)
        self.frm_plot = tk.Frame(master=self.frm_top)
        self.frm_controls = tk.Frame()
        self.fig = Figure()
        self.init_plot()
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frm_plot)
        
        self.btn_launch = tk.Button(text='Launch', command=self.launch, master=self.frm_controls)
        self.btn_pause = tk.Button(text='Pause',command=self.pause, master=self.frm_controls)
        self.btn_next = tk.Button(text='Next', master=self.frm_controls)
        
    
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.btn_pause.pack(side=tk.LEFT)
        self.btn_launch.pack(side=tk.LEFT)
        self.frm_stats.pack(side=tk.LEFT)
        self.frm_plot.pack(side=tk.RIGHT)
        self.frm_top.pack(side=tk.TOP)
        self.frm_controls.pack(side=tk.BOTTOM, expand=True)

    def init_plot(self):
        self.ax = self.fig.add_subplot(111)
        self.frame = self.ax.imshow(self.sim.env.get_grid(self.plot_stgs), interpolation="none", cmap="gist_ncar", animated=True)
        self.ax.set_xticks([])
        self.ax.set_yticks([])


    def updatefig(self, i):
        if (not i % self.plot_stgs.show_n) and (not self.paused):
            self.sim.next()
        self.frame.set_array(self.sim.env.get_grid(self.plot_stgs))
        return self.frame, 
    
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
            self.btn_launch.config(text='Restart')
            self.ani.resume()  
        else: 
            self.btn_launch.config(text='Launch')
            self.ani.pause()
            self.sim.restart()

    def pause(self):
        self.paused ^= True
        button_txt = 'Resume' if self.paused else 'Pause'
        self.btn_pause.config(text=button_txt)



gui = GUI(default_envrule, default_cellrule, default_plotrule)

gui.start()
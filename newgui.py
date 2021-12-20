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

root = tk.Tk()
root.title("Cell Simulation")

sim = Simulation(default_envrule, default_cellrule)
plot_stgs = getattr(plot_rules, default_plotrule)()


fig = Figure()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
ax = fig.add_subplot(111)
frame = ax.imshow(sim.env.get_grid(plot_stgs), interpolation="none", cmap="gist_ncar", animated=True)

def updatefig(i):
    sim.next()
    frame.set_array(sim.env.get_grid(plot_stgs))
    return frame,

ani = animation.FuncAnimation(fig, updatefig, interval=plot_stgs.fps, blit=True)

root.mainloop()

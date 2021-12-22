import time, yaml
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg

from src.main_thread import MainThread
from src.simulation import Simulation
import archive.option_windows as opt_win

matplotlib.use('TkAgg')

with open("parameters/config.yaml", "r") as f:
    config = yaml.safe_load(f)
    
default_envrule = config["default_envrule"]
default_cellrule = config["default_cellrule"]
default_plotrule = config["default_plotrule"]

main = MainThread(default_envrule, default_cellrule, default_plotrule)
main.next()

while True:
    event, values = main.window.read()
    
    if event == sg.WIN_CLOSED:
        break
    
    if event == 'Next' or event == 'right':
        main.next()

    if event == 'Launch':
        main.launch()
    
    if event == 'Pause':
        main.pause()

    if event == 'Parameters':
        main.pause()
        new_params = opt_win.change_params(main.sim) 
        main.resume()

    if event == 'Environment Rule':
        main.pause()
        new_envrule = opt_win.choose_rule(chosen_env_rule=main.sim.envrule)
        main.sim.update_rules(new_envrule=new_envrule)
        main.resume()

    if event == 'Cells Rule':
        main.pause()
        new_cellrule = opt_win.choose_rule(chosen_cell_rule=main.sim.cellrule)
        main.sim.update_rules(new_cellrule=new_cellrule) 
        main.resume()

    if event == 'Plotting':
        main.pause()
        opt_win.plotting(main.plot_stgs)
        main.resume()

main.window.close()
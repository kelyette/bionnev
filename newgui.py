import time, yaml
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg

from src.main_thread import MainThread
from src.simulation import Simulation
import src.option_windows as opt_win

matplotlib.use('TkAgg')

with open("parameters/config.yaml", "r") as f:
    config = yaml.safe_load(f)
    
default_envrule = config["default_envrule"]
default_cellrule = config["default_cellrule"]

main = MainThread(default_envrule, default_cellrule)

while True:
    event, values = main.window.read()
    
    if event == sg.WIN_CLOSED:
        break
    
    if event == 'Next' or event == 'right':
        main.run_once()

    if event == 'Launch':
        main.start()

    if event == 'Parameters':
        new_params = opt_win.change_params(main.sim) 

    if event == 'Environment Rule':
        new_envrule = opt_win.choose_rule(chosen_env_rule=main.sim.envrule)
        main.sim.update_rules(new_envrule=new_envrule)

    if event == 'Cells Rule':
        new_cellrule = opt_win.choose_rule(chosen_cell_rule=main.sim.cellrule)
        main.sim.update_rules(new_cellrule=new_cellrule) 

    if event == 'Plotting':
        opt_win.plotting(main.plot_stgs)

main.window.close()
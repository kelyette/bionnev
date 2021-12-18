import threading
import time, yaml
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg

from src.main_thread import MainThread
from src.simulation import Simulation
from src.parameters import Params

matplotlib.use('TkAgg')

with open("parameters/config.yaml", "r") as f:
    config = yaml.safe_load(f)
    
default_envrule = config["default_envrule"]
default_cellrule = config["default_cellrule"]

sg.theme('SystemDefault1')
font = ('Helvetica', 12)
titlefont = ('Helvetica', 14, "bold")
figsize = (50, 50)
menu_layout = [
    ["Simulation", ["Launch Simulation"]],
    ["Edit Simulation", ["Params", "Environment", "Cells"]],
    ["Plotting"],
    ["Defaults"],
]

layout = [
   [sg.MenuBar(menu_layout)],
   [sg.Canvas(canvas=None)],
]

main = MainThread(default_envrule, default_cellrule)

while True:
    event, values = main.window.read()
    
    if event == sg.WIN_CLOSED:
        break
    
main.window.close()
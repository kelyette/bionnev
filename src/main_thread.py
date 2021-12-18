from src.simulation import Simulation
import threading

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg

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
        
    def sg_init(self):
        sg.theme('SystemDefault1')
        self.font = ('Helvetica', 12)
        self.titlefont = ('Helvetica', 14, "bold")
        self.figsize = (50, 50)
        menu_layout = [
            ["Simulation", ["Launch Simulation"]],
            ["Edit Simulation", ["Params", "Environment", "Cells"]],
            ["Plotting"],
            ["Defaults"],
        ]
        
        layout = [
            [sg.MenuBar(menu_layout)],
            [sg.Canvas(canvas=None)],
            [sg.Button("Start", key="start")] 
        ]
        
        self.window = sg.Window("Oui", layout, font=self.font, finalize=True, resizable=True)
    
    def sg_change_params(self):
        pass
    
    def run(self):
        while self.__running.is_set():
            self.__flag.wait()
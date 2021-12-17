import threading
import yaml, time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg

from src.simulation import Simulation
from src.parameters import Params

matplotlib.use('TkAgg')

params = Params()

doLoop = False

sg.theme('SystemDefault1')
font = ('Helvetica', 12)
titlefont = ('Helvetica', 14, "bold")
figsize = (5, 5)

def plot(fig, grid, env):
    if fig:
        plt.clf()
        fig.get_tk_widget().forget()
    if grid is None:
        fig = matplotlib.figure.Figure(figsize=figsize)
        fig.add_subplot(111)
        return fig
        
    plt.title(f"Epoch {env.clock}")
    plt.imshow(grid, interpolation="none", cmap="gist_ncar", vmin=0, vmax=len(params.colors))
    return plt.gcf()

def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

class plot_loop(threading.Thread):
    def __init__(self, sim, window, fig):
        super(plot_loop, self).__init__()
        self.__flag = threading.Event() # The flag used to pause the thread
        self.__flag.set() # Set to True
        self.__running = threading.Event() # Used to stop the thread identification
        self.__running.set() # Set running to True
        self.bool_resume = False
        self.daemon = True
        self.sim = sim
        self.window = window
        self.fig = fig

    def run(self):
        self.bool_resume = True  
        while self.__running.isSet():
            self.__flag.wait()
            self.sim.next()
            self.fig = draw_figure(self.window['plot'].TKCanvas, plot(self.fig, self.sim.env.get_grid(), self.sim.env))
            time.sleep(0.1)

    def run_once(self):
        self.sim.next()
        self.fig = draw_figure(self.window['plot'].TKCanvas, plot(self.fig, self.sim.env.get_grid(), self.sim.env))

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
        self.bool_resume = True

def choose_rule(rule_dict, chosen_rule, title):
    rule_left_layout = [
        [sg.Text("All available rules", font=titlefont)],
        [sg.Listbox([rule for rule in rule_dict.keys()], default_values=chosen_rule, key='selected_rule', select_mode=sg.SELECT_MODE_SINGLE, size=(10, 10), enable_events=True)],
    ]
    rule_right_layout = [
        [sg.Text("Explanation", font=titlefont)],
        [sg.Multiline(rule_dict[chosen_rule]['exp'], size=(40, 8), key='explanation')],
        [sg.Text(" ", size=(35, 1)), sg.Button('Choose', enable_events=True)]
    ]
    rule_layout = [
        [sg.Column(rule_left_layout), sg.Column(rule_right_layout)]
    ]
    rule_window = sg.Window(title, rule_layout, font=font)
    while True:
        rule_event, rule_values = rule_window.read()
        if rule_event == sg.WIN_CLOSED:
            break
        elif rule_event == 'Choose':
            chosen_rule = rule_values['selected_rule'][0]
            break
        elif rule_values['selected_rule'][0] != chosen_rule:
            chosen_rule = rule_values['selected_rule'][0]
            rule_window.Element('explanation').Update(value=rule_dict[chosen_rule]['exp'])
    rule_window.close()
    return chosen_rule

def change_params(params, env_rule, cell_rule):
    bool_params = [params.env_rules_dict[env_rule]['params'][i] + params.cell_rules_dict[cell_rule]['params'][i] for i in range(len(params.cell_rules_dict[cell_rule]['params']))]
    needed_params = {list(params.keys())[i]: params[list(params.keys())[i]] for i in range(len(bool_params)) if bool_params[i]}
    selected_key = list(needed_params.keys())[0]

    params_left_layout = [
        [sg.Text("All available parameters", font=titlefont)],
        [sg.Listbox([rule for rule in needed_params.keys()], default_values=selected_key, key='selected_key', select_mode=sg.SELECT_MODE_SINGLE, size=(10, 10), enable_events=True)],
    ]
    params_right_layout = [
        [sg.Text("Value", font=titlefont)],
        [sg.Text("Modify:"), sg.Input(default_text=needed_params[selected_key], key='value', enable_events=True)],
        [sg.Text("Explanation", font=titlefont)],
        [sg.Multiline(params[selected_key], size=(40, 8), key='explanation')],
        [sg.Button('Exit'), sg.Button('Save Changes')],
    ]
    params_layout = [
        [sg.Column(params_left_layout), sg.Column(params_right_layout)]
    ]
    params_window = sg.Window("Parameters", params_layout, font=font)
    changes = False
    while True:
        params_event, params_values = params_window.read()
        if params_event == sg.WIN_CLOSED or params_event == 'Exit':
            # FAIRE UN POPUP POUR CONFIRMER DES
            break
        elif params_values['selected_key'][0] != selected_key:
            selected_key = params_values['selected_key'][0]
            params_window.Element('value').Update(value=needed_params[selected_key])
            params_window.Element('explanation').Update(value=params_exp[selected_key])
            
        elif params_values['value'] != str(needed_params[selected_key]):
            needed_params[selected_key] = float(params_values['value'])
                
        elif params_event == 'Save Changes':
            for k in list(needed_params.keys()):
                params[k] = needed_params[k]
            break
    params_window.close()
    return params


main_left_layout = [
    [sg.Text("Simulation Parameters", font=titlefont)],
    [sg.Text("Enviroment rule set:  ", font=font, size=(15, 1)), sg.Multiline(default_text=params.env_rule_key, font=font, key='chosen_env_rule', size=(15, 1), no_scrollbar=True), sg.Button("Choose", key='env_rule')],
    [sg.Text("Cell rule set:  ", font=font, size=(15, 1)), sg.Multiline(default_text=params.cell_rule_key, font=font, key='chosen_cell_rule', size=(15, 1), no_scrollbar=True), sg.Button("Choose", key='cell_rule')],
    [sg.Text("Parameters:  ", font=font, size=(15, 1)), sg.Button("Modify", key='params')],
    [sg.Text("Controls", font=titlefont)],
    [sg.Button("Prec"), sg.Button("Next"), sg.Button("Restart"), sg.Button("Pause"), sg.Button("Play")]
]
main_right_layout = [
    [sg.Canvas(size=(10, 10), key="plot")],
]
main_layout = [
    [sg.Column(main_left_layout), sg.Column(main_right_layout)]
]
window = sg.Window("Cells Evolution Simulator", main_layout, finalize=True, font=font, resizable=True, location=(20, 20))

def main():
    global t
    global params
    
    sim = Simulation(params)
    fig = draw_figure(window['plot'].TKCanvas, plot(None, None, None))
    t = plot_loop(sim, window, fig)
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'env_rule':
            chosen_env_rule = values['chosen_env_rule']
            chosen_env_rule = choose_rule(params.env_rules_dict, chosen_env_rule, "Environment Rule Selection")
            window.Element('chosen_env_rule').Update(value=chosen_env_rule)
            sim.update_rules(new_envrule=params.env_rules_dict[chosen_env_rule]['fun'])
            
        elif event == 'cell_rule':
            chosen_cell_rule = values['chosen_cell_rule']
            chosen_cell_rule = choose_rule(params.cell_rules_dict, chosen_cell_rule, "Cell Rule Selection")
            window.Element('chosen_cell_rule').Update(value=chosen_cell_rule)
            sim.update_rules(new_cellrule=params.cell_rules_dict[chosen_cell_rule]['fun'])

        elif event == 'params':
            params.list = change_params(params.list, values['chosen_env_rule'], values['chosen_cell_rule'])
            params.list = params.get_mean_std(params.list)
            del sim
            sim = Simulation(params)

        elif event == 'Next':
            t.run_once()
            
        elif event == 'Play':
            if t.bool_resume:
                t.resume()
            else:
                t.start()
            
        elif event == 'Pause':
            t.pause()

    window.close()

if __name__ == '__main__':
    main()
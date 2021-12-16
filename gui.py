from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PySimpleGUI.PySimpleGUI import SELECT_MODE_SINGLE
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import yaml
matplotlib.use('TkAgg')

with open("params.yaml", "r") as f:
    all_params = yaml.safe_load(f)
    params = all_params['values']
    params_exp = all_params['exp']

with open("env_rules.yaml", "r") as f:
    env_rules = yaml.safe_load(f)
default_env_rule = list(env_rules.keys())[0]

with open("cell_rules.yaml", "r") as f:
    cell_rules = yaml.safe_load(f)
default_cell_rule = list(cell_rules.keys())[0]

sg.theme('SystemDefault1')
font = ('Helvetica', 12)
titlefont = ('Helvetica', 14, "bold")
figsize = (5, 5)


def plot(fig, grid):
    if fig is not None:
        fig.get_tk_widget().forget()
    fig = matplotlib.figure.Figure(figsize=figsize)
    fig.add_subplot(111)
    if grid is None:
        return fig
    plt.imshow(grid, interpolation="none", cmap="GnBu")
    

def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def choose_rule(rule_dict, chosen_rule, title):
    rule_left_layout = [
        [sg.Text("All available rules", font=titlefont)],
        [sg.Listbox([rule for rule in rule_dict.keys()], default_values=chosen_rule, key='selected_rule', select_mode=SELECT_MODE_SINGLE, size=(10, 10), enable_events=True)],
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
    bool_params = [env_rules[env_rule]['params'][i] + cell_rules[cell_rule]
                   ['params'][i] for i in range(len(cell_rules[cell_rule]['params']))]
    needed_params = {list(params.keys())[i]: params[list(params.keys())[
        i]] for i in range(len(params)) if bool_params[i]}
    selected_key = list(needed_params.keys())[0]

    params_left_layout = [
        [sg.Text("All available parameters", font=titlefont)],
        [sg.Listbox([rule for rule in needed_params.keys()], default_values=selected_key, key='selected_key', select_mode=SELECT_MODE_SINGLE, size=(10, 10), enable_events=True)],
    ]
    params_right_layout = [
        [sg.Text("Value", font=titlefont)],
        [sg.Text("Modify:"), sg.Input(default_text=needed_params[selected_key], key='value', enable_events=True)],
        [sg.Text("Explanation", font=titlefont)],
        [sg.Multiline(params_exp[selected_key], size=(40, 8), key='explanation')],
        [sg.Button('Exit'), sg.Button('Save Changes')],
    ]
    params_layout = [
        [sg.Column(params_left_layout), sg.Column(params_right_layout)]
    ]
    params_window = sg.Window("Parameters", params_layout, font=font)
    while True:
        params_event, params_values = params_window.read()
        if params_event == sg.WIN_CLOSED or params_event == 'Exit':
            # FAIRE UN POPUP POUR CONFIRMER DES
            break
        elif params_values['selected_key'][0] != selected_key:
            selected_key = params_values['selected_key'][0]
            params_window.Element('value').Update(value=needed_params[selected_key])
            params_window.Element('explanation').Update(value=params_exp[selected_key])
            
        elif params_values['value'] != needed_params[selected_key]:
            try:
                new_value = int(params_values['value']) if int(params_values['value']) == float(
                    params_values['value']) else float(params_values['value'])
                if isinstance(new_value, type(needed_params[selected_key])):
                    needed_params[selected_key] = params_values['value']
                else:
                    sg.popup_error(
                        f"The value you inputted must be {type(needed_params[selected_key])}, not {type(new_value)}")
            except:
                sg.popup_error(
                    f"The value you inputted cannot be transformed into a number.")
        elif params_event == 'Save Changes':
            for k in list(needed_params.keys()):
                params[k] = needed_params[k]
    params_window.close()
    return params


main_left_layout = [
    [sg.Text("Simulation Parameters", font=titlefont)],
    [sg.Text("Enviroment rule set:  ", font=font, size=(15, 1)), sg.Multiline(default_text=default_env_rule, font=font, key='chosen_env_rule', size=(15, 1), no_scrollbar=True), sg.Button("Choose", key='env_rule')],
    [sg.Text("Cell rule set:  ", font=font, size=(15, 1)), sg.Multiline(default_text=default_cell_rule, font=font, key='chosen_cell_rule', size=(15, 1), no_scrollbar=True), sg.Button("Choose", key='cell_rule')],
    [sg.Text("Parameters:  ", font=font, size=(15, 1)), sg.Button("Modify", key='params')],
    [sg.Button("Launch simulation")],
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

fig = draw_figure(window['plot'].TKCanvas, plot(None, None))

sim = Simulation(params)

def main():
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'env_rule':
            chosen_rule = values['chosen_env_rule']
            chosen_rule = choose_rule(env_rules, chosen_rule, "Environment Rule Selection")
            window.Element('chosen_env_rule').Update(value=chosen_rule)
            sim.update_rules(new_envrule=chosen_rule)

        elif event == 'cell_rule':
            chosen_rule = values['chosen_cell_rule']
            chosen_rule = choose_rule(cell_rules, chosen_rule, "Cell Rule Selection")
            window.Element('chosen_cell_rule').Update(value=chosen_rule)
            sim.update_rules(new_envrule=chosen_rule)

        elif event == 'params':
            params = change_params(params, values['chosen_env_rule'], values['chosen_cell_rule'])
            sim.update_params(params)

        elif event == 'Next':
            sim.next()
            fig = draw_figure(window['plot'].TKCanvas, plot(fig, sim.get_grid()))

    window.close()

if __name__ == '__main__':
    main()

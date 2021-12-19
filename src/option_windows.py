import PySimpleGUI as sg
import inspect
import src.rules.cell_rules as cr
import src.rules.env_rules as er

sg.theme('SystemDefault1')
font = ('Helvetica', 12)
titlefont = ('Helvetica', 14, "bold")

def choose_rule(chosen_env_rule=None, chosen_cell_rule=None):
    if chosen_env_rule:
        chosen_rule = chosen_env_rule
        available_rules = inspect.getmembers(er, inspect.isclass)[2:]
        title = "Environment Rule Selection"
    if chosen_cell_rule:
        chosen_rule = chosen_cell_rule
        available_rules = inspect.getmembers(cr, inspect.isclass)[1:]
        title = "Cell Rule Selection"
    rule_exps = {rule[1]().display_name: rule[1]().exp for rule in available_rules}
    
    rule_left_layout = [
        [sg.Text("All available rules", font=titlefont)],
        [sg.Listbox([rule[1]().display_name for rule in available_rules], default_values=chosen_rule.display_name, key='selected_rule', select_mode=sg.SELECT_MODE_SINGLE, size=(10, 10), enable_events=True)],
    ]
    rule_right_layout = [
        [sg.Text("Explanation", font=titlefont)],
        [sg.Multiline(rule_exps[chosen_rule.display_name], size=(40, 8), key='explanation')],
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
        elif rule_values['selected_rule'][0] != chosen_rule.display_name:
            chosen_rule = next((r for r in available_rules if r[1]().display_name == rule_values['selected_rule'][0]), None)[1]()
            rule_window.Element('explanation').Update(value=rule_exps[chosen_rule.display_name])
        elif rule_event == 'Choose':
            break
    rule_window.close()

    return chosen_rule

def change_params(sim):
    params_exp = dict(sim.env.envrule.params_exp, **sim.env.cellrule.params_exp)
    params = dict(sim.env.envrule.params, **sim.env.cellrule.params)
    params = {k: params[k] for k in params_exp}
    selected_key = list(params.keys())[0]
    
    params
    
    params_left_layout = [
        [sg.Text("All available parameters", font=titlefont)],
        [sg.Listbox([param for param in params.keys()], default_values=selected_key, key='selected_key', select_mode=sg.SELECT_MODE_SINGLE, size=(10, 10), enable_events=True)],
    ]
    params_right_layout = [
        [sg.Text("Value", font=titlefont)],
        [sg.Text("Modify:"), sg.Input(default_text=params[selected_key], key='value', enable_events=True)],
        [sg.Text("Explanation", font=titlefont)],
        [sg.Multiline(params_exp[selected_key], size=(40, 8), key='explanation')],
        [sg.Button('Exit'), sg.Button('Save Changes')],
    ]
    params_layout = [
        [sg.Column(params_left_layout), sg.Column(params_right_layout)]
    ]
    params_window = sg.Window("Parameters", params_layout, font=font)
    modified = False
    while True:
        params_event, params_values = params_window.read()
        if params_event == sg.WIN_CLOSED or params_event == 'Exit':
            if params_values['value'] != str(params[selected_key]):
                params[selected_key] = float(params_values['value'])
            changed_params = ""
            for k in list(params.keys()):
                if k in sim.env.envrule.params.keys():
                    if sim.env.envrule.params[k] != params[k]:
                        changed_params += f"{k} from {sim.env.envrule.params[k]} to {params[k]},"
                if k in sim.env.cellrule.params.keys():
                    if sim.env.cellrule.params[k] != params[k]:
                        changed_params += f"{k} from {sim.env.cellrule.params[k]} to {params[k]},"
            if len(changed_params):
                sg.popup("Are you sure? You have the following changes:\n " + changed_params[:-1], title='Unsaved changes')
            break
        elif params_values['selected_key'][0] != selected_key:
            params[selected_key] = float(params_values['value'])
            selected_key = params_values['selected_key'][0]
            params_window.Element('value').Update(value=params[selected_key])
            params_window.Element('explanation').Update(value=params_exp[selected_key])
                
        elif params_event == 'Save Changes':
            for k in list(params.keys()):
                if k in sim.env.envrule.params.keys():
                    sim.env.envrule.params[k] = params[k]
                if k in sim.env.cellrule.params.keys():
                    sim.env.cellrule.params[k] = params[k]
            break
    params_window.close()
import numpy as np
import tkinter as tk
import inspect
import parameters.env_rules as er
import parameters.cell_rules as cr
import parameters.plot_rules as pr

rgb2hex = lambda r,g,b: '#%02x%02x%02x' %(r,g,b)
hex2rgb = lambda hex: tuple(int(hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))


class Settings:
    def __init__(self, chosen_envrule, chosen_cellrule, chosen_plotrule):
        self.chosen_envrule = chosen_envrule
        self.chosen_cellrule = chosen_cellrule
        self.chosen_plotrule = chosen_plotrule
        self.win = tk.Toplevel()
        self.win.title("Settings")


    def get_rules(self):
        self.envrules = inspect.getmembers(er, inspect.isclass)[2:]
        self.envrule_exps = {rule[1]().display_name: rule[1]().exp for rule in self.envrules}
        self.cellrules = inspect.getmembers(cr, inspect.isclass)[2:]
        self.cellrule_exps = {rule[1]().display_name: rule[1]().exp for rule in self.cellrules}
        self.plotrules = inspect.getmembers(pr, inspect.isclass)[2:]
        self.plotrule_exps = {rule[1]().display_name: rule[1]().exp for rule in self.plotrules}
        # self.params_exp = dict(sim.env.envrule.params_exp, **sim.env.cellrule.params_exp)
        # params = dict(sim.env.envrule.params, **sim.env.cellrule.params)
        # params = {k: params[k] for k in params_exp}
        # selected_key = list(params.keys())[0]

    
settings = Settings(None, None, None)
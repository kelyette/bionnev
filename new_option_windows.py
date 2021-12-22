import numpy as np
import tkinter as tk
from tkinter import ttk
import inspect

from numpy.core.fromnumeric import size
import parameters.env_rules as er
import parameters.cell_rules as cr
import parameters.plot_rules as pr

rgb2hex = lambda r,g,b: '#%02x%02x%02x' %(r,g,b)
hex2rgb = lambda hex: tuple(int(hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))



class Settings:
    def __init__(self, sim, chosen_plotrule):
        self.sim = sim
        self.chosen_envrule = self.sim.envrule
        self.chosen_cellrule = self.sim.cellrule
        self.chosen_plotrule = chosen_plotrule

        self.get_rules()
        self.init_window()


    def get_rules(self):
        self.envrules = inspect.getmembers(er, inspect.isclass)[2:]
        self.envrule_exps = {rule[1]().display_name: rule[1]().exp for rule in self.envrules}
        self.cellrules = inspect.getmembers(cr, inspect.isclass)[2:]
        self.cellrule_exps = {rule[1]().display_name: rule[1]().exp for rule in self.cellrules}
        self.plotrules = inspect.getmembers(pr, inspect.isclass)[2:]
        self.plotrule_exps = {rule[1]().display_name: rule[1]().exp for rule in self.plotrules}


    def init_window(self):
        self.win = tk.Toplevel()
        self.win.title("Settings")
        self.tabControl = ttk.Notebook(self.win)

        self.init_gen_tab()
        self.init_env_tab()
        self.init_cell_tab()
        self.init_plot_tab()

        self.tabControl.pack(expand=1, fill="both")
    
    def init_gen_tab(self):
        self.tab_gen = ttk.Frame(self.tabControl)
        lbl_title = ttk.Label(text='Default Rules',master=self.tab_gen)
        lbl_title.pack(side=tk.TOP, anchor=tk.NW)

        self.tabControl.add(self.tab_gen, text='General')

    def init_env_tab(self):
        self.tab_env = ttk.Frame(self.tabControl)
        frm_rules = tk.Frame(self.tab_env)
        frm_params = tk.Frame(self.tab_env)
        frm_controls = tk.Frame(self.tab_env)

        self.set_select_n_exp(frm_rules, self.envrules, self.envrule_exps, 'lb_envrule', 'msg_envrule_exp', 'Rules')
        
        frm_rules.pack(side=tk.TOP)
        frm_params.pack(side=tk.TOP)
        frm_controls.pack(side=tk.TOP)
        self.tabControl.add(self.tab_env, text='Environment')

    def init_cell_tab(self):
        self.tab_cell = ttk.Frame(self.tabControl)
        frm_rules = tk.Frame(self.tab_cell)
        frm_params = tk.Frame(self.tab_cell)
        frm_controls = tk.Frame(self.tab_cell)

        self.set_select_n_exp(frm_rules, self.cellrules, self.cellrule_exps, 'lb_cellrule', 'msg_cellrule_exp', 'Rules')

        frm_rules.pack(side=tk.TOP)
        frm_params.pack(side=tk.TOP)
        frm_controls.pack(side=tk.TOP)
        self.tabControl.add(self.tab_cell, text='Cells')    

    def init_plot_tab(self):
        self.tab_plot = ttk.Frame(self.tabControl)
        frm_rules = tk.Frame(self.tab_plot)
        frm_params = tk.Frame(self.tab_plot)
        frm_controls = tk.Frame(self.tab_plot)

        self.set_select_n_exp(frm_rules, self.plotrules, self.plotrule_exps, 'lb_plotrule', 'msg_plotrule_exp', 'Plotting')

        frm_rules.pack(side=tk.TOP)
        frm_params.pack(side=tk.TOP)
        frm_controls.pack(side=tk.TOP)
        self.tabControl.add(self.tab_plot, text='Plotting')

    def set_select_n_exp(self, master, rule_list, exp_dict, rule_var, rule_var_exp, title):
        frm_left = tk.Frame(master)
        frm_right = tk.Frame(master)
        lbl_title_left = tk.Label(master=frm_left, text=title)
        setattr(self, rule_var, tk.Listbox(frm_left, height=10))
        for i, rule in enumerate(rule_list):
            getattr(self, rule_var).insert(i+1, rule[1]().display_name)
        getattr(self, rule_var).bind('<<ListboxSelect>>', lambda x: self.change_exp(x, rule_var_exp, exp_dict))
        lbl_title_right = tk.Label(master=frm_right, text='Explanation')
        setattr(self, rule_var_exp, tk.Message(master=frm_right, text=f""))
        lbl_title_left.pack(side=tk.TOP, anchor=tk.NW)
        getattr(self, rule_var).pack(side=tk.TOP, fill=tk.BOTH)
        lbl_title_right.pack(side=tk.TOP, anchor=tk.NW)
        getattr(self, rule_var_exp).pack(side=tk.TOP, fill=tk.BOTH)
        frm_left.pack(side=tk.LEFT)
        frm_right.pack(side=tk.RIGHT)
    
    #def set_controls(self):


    def change_exp(self, evt, exp_box, exp_dict):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        getattr(self, exp_box).config(text=exp_dict[value])

    def start(self):
        self.win.mainloop()


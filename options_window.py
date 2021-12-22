import numpy as np
import tkinter as tk
from tkinter import ttk
import inspect

from numpy.core.fromnumeric import size
import parameters.env_rules as er
import parameters.cell_rules as cr
import parameters.plot_rules as pr

rgb2hex = lambda r,g,b: '#%02x%02x%02x' % (r,g,b)
hex2rgb = lambda hex: tuple(int(hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))



class Settings:
    def __init__(self, sim, chosen_plotrule):
        self.sim = sim
        self.chosen_envrule = self.sim.envrule
        self.chosen_cellrule = self.sim.cellrule
        self.chosen_plotrule = chosen_plotrule
        
        self.update_selected(self.chosen_envrule, self.chosen_cellrule, self.chosen_plotrule)

        self.get_rules()
        self.init_window()


    def get_rules(self):
        self.envrules = inspect.getmembers(er, inspect.isclass)[2:]
        self.envrule_exps = {rule[1]().display_name: rule[1]().exp for rule in self.envrules}
        self.cellrules = inspect.getmembers(cr, inspect.isclass)[2:]
        self.cellrule_exps = {rule[1]().display_name: rule[1]().exp for rule in self.cellrules}
        self.plotrules = inspect.getmembers(pr, inspect.isclass)[2:]
        self.plotrule_exps = {rule[1]().display_name: rule[1]().exp for rule in self.plotrules}

    def update_selected(self, new_selected_envrule=None, new_selected_cellrule=None, new_selected_plotrule=None):
        if new_selected_envrule:
            self.selected_envrule = new_selected_envrule
            self.selected_envrule_params = self.selected_envrule.params
            self.selected_envrule_params_exp = self.selected_envrule.params_exp
        if new_selected_cellrule:
            self.selected_cellrule = new_selected_cellrule
            self.selected_cellrule_params = self.selected_cellrule.params
            self.selected_cellrule_params_exp = self.selected_cellrule.params_exp
        if new_selected_plotrule:
            self.selected_plotrule = new_selected_plotrule
            self.selected_plotrule_params = {'fps': self.selected_plotrule.fps, 'show_n': self.selected_plotrule.show_n}
            self.selected_plotrule_params_exp = {'fps': 'Number of frames per second (rapidity of the animation)', 'show_n': 'Shows only every nth simulation day'}

    def init_window(self):
        self.win = tk.Toplevel()
        self.win.title("Settings")
        self.tabControl = ttk.Notebook(self.win)

        self.init_env_tab()
        self.init_cell_tab()
        self.init_plot_tab()

        self.tabControl.pack(expand=1, fill="both")

    
    def init_env_tab(self):
        self.tab_env = ttk.Frame(self.tabControl)
        frm_rules = tk.Frame(self.tab_env)
        frm_params = tk.Frame(self.tab_env)
        frm_controls = tk.Frame(self.tab_env)

        self.selection_frame(frm_rules, 'env')
        self.set_controls(frm_controls)
        
        frm_rules.pack(side=tk.TOP)
        frm_params.pack(side=tk.TOP)
        frm_controls.pack(side=tk.TOP)
        self.tabControl.add(self.tab_env, text='Environment')

    def init_cell_tab(self):
        self.tab_cell = ttk.Frame(self.tabControl)
        frm_rules = tk.Frame(self.tab_cell)
        frm_params = tk.Frame(self.tab_cell)
        frm_controls = tk.Frame(self.tab_cell)

        self.selection_frame(frm_rules, 'cell')
        self.set_controls(frm_controls)

        frm_rules.pack(side=tk.TOP)
        frm_params.pack(side=tk.TOP)
        frm_controls.pack(side=tk.TOP)
        self.tabControl.add(self.tab_cell, text='Cells')    

    def init_plot_tab(self):
        self.tab_plot = ttk.Frame(self.tabControl)
        frm_rules = tk.Frame(self.tab_plot)
        frm_params = tk.Frame(self.tab_plot)
        frm_controls = tk.Frame(self.tab_plot)

        self.selection_frame(frm_rules, 'plot')
        self.set_controls(frm_controls)

        frm_rules.pack(side=tk.TOP)
        frm_params.pack(side=tk.TOP)
        frm_controls.pack(side=tk.TOP)
        self.tabControl.add(self.tab_plot, text='Plotting')

    def selection_frame(self, master, tab):
        if tab == 'env':
            rules = self.envrules
            rules_exp = self.envrule_exps
        if tab == 'cell':
            rules = self.cellrules
            rules_exp = self.cellrule_exps
        if tab == 'plot':
            rules = self.plotrules
            rules_exp = self.plotrule_exps
        rule_var = 'selection_' + tab + 'rule'
        rule_var_exp = 'shown_' + tab + 'rule_exp'
        frm_left = tk.Frame(master)
        frm_right = tk.Frame(master)

        lbl_title_section = tk.Label(master=frm_left, text='BONSOIR')
        lbl_title_left = tk.Label(master=frm_left, text='Rules List')
        setattr(self, rule_var, tk.Listbox(frm_left, height=10))
        for i, rule in enumerate(rules):
            getattr(self, rule_var).insert(i+1, rule[1]().display_name)
        getattr(self, rule_var).bind('<<ListboxSelect>>', lambda x: self.change_selected(x, tab, rule_var_exp, rules_exp))

        lbl_title_right = tk.Label(master=frm_right, text='Explanation')
        setattr(self, rule_var_exp, tk.Message(master=frm_right, text=f"", borderwidth=10))


        lbl_title_section.pack(side=tk.TOP, anchor=tk.NW)
        lbl_title_left.pack(side=tk.TOP, anchor=tk.NW)
        getattr(self, rule_var).pack(side=tk.TOP, fill=tk.BOTH)

        lbl_title_right.pack(side=tk.TOP, anchor=tk.NW)
        getattr(self, rule_var_exp).pack(side=tk.TOP, fill=tk.BOTH)

        frm_left.pack(side=tk.LEFT)
        frm_right.pack(side=tk.RIGHT)
    
    def set_controls(self, master):
        frm_top = tk.Frame(master)
        frm_bottom = tk.Frame(master)
        btn_set = tk.Button(master = frm_top, text="Set Rule & Parameters")
        btn_set_rule_def =tk.Button(master = frm_bottom, text="Save Rule as Default")
        btn_save_params_def = tk.Button(master = frm_bottom, text="Save Parameters as Default")

        btn_save_params_def.pack(side=tk.RIGHT, anchor=tk.E)
        btn_set_rule_def.pack(side=tk.RIGHT, anchor=tk.E)
        btn_set.pack(side=tk.RIGHT, anchor=tk.E)
        frm_top.pack(side=tk.TOP, anchor=tk.E)
        frm_bottom.pack(side=tk.BOTTOM)

    def change_selected(self, evt, tab,  exp_box, rules_exp):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        chosen_rule = next((r[1]() for r in getattr(self, tab +'rules') if r[1]().display_name == value))
        self.update_selected(**{'new_selected_' + tab + 'rule': chosen_rule})
        getattr(self, exp_box).config(text=rules_exp[value])

    def start(self):
        self.win.mainloop()


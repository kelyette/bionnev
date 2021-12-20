from tkinter.constants import X
import numpy as np
from src.cell import Cell

class CellRule:
    def __init__(self):
        if hasattr(self,'display_name') and hasattr(self,'exp') and  hasattr(self,'params_dict') and hasattr(self,'num_sensors') and hasattr(self,'num_actions') and hasattr(self,'phys_attr'):
            self.__class__.params = {}
            self.__class__.params_exp = {}

            for key in self.params_dict.keys():
                try:
                    self.__class__.params[key] = self.params_dict[key]["val"]
                except:
                    raise ValueError("Each parameters in params_dict must be a dict with its 'val' (value) and 'exp' (explanation).")
                try:
                    self.__class__.params_exp[key] = self.params_dict[key]["exp"]
                except:
                    raise ValueError("Each parameters in params_dict must be a dict with its 'val' (value) and 'exp' (explanation).")
            self.build_phys()
            self.set_all_other_attr()
            self.check_cell_function()
        else:
            raise AttributeError(f"Cellrule class must have the following attributes {['display_name', 'exp', 'params_dict', 'num_sensors', 'num_actions', 'phys_attr']} set in its init function.")

    def build_phys(self):
        if 'death' not in self.phys_attr:
            raise AttributeError(f"Cellrule class attribute phys_attr should have 'death'")
        else:
            if 'mean_death' not in list(self.params_dict.keys()) or 'std_death' not in list(self.params_dict.keys()) :
                raise AttributeError(f"Cellrule class attribute params_dict should have ['mean_death', 'std_death']")
            else: 
                mean_phys_params = []
                std_phys_params = []
                for i, attr in enumerate(self.phys_attr):
                    try:
                        mean_phys_params.append(self.params[f"mean_{attr}"])
                    except:
                        raise ValueError(f"mean_{attr} should exist in params_dict.")
                    try:
                        std_phys_params.append(self.params[f"std_{attr}"])
                    except:
                        raise ValueError(f"std_{attr} should exist in params_dict.")
                self.params['mean_physics'] = np.array(mean_phys_params)
                self.params['std_physics'] = np.array(std_phys_params)
                
        
    def set_all_other_attr(self):
        self.other_attr = {}
        for attr in list(self.params.keys()):
            is_phys_param = False
            for phys_attr in self.phys_attr + ['mean_physics', 'std_physics']:
                if phys_attr in attr:
                    is_phys_param = True
            if not is_phys_param:
                self.other_attr[attr] = self.params[attr]
                
                    

    def check_cell_function(self):
        if hasattr(self, 'cell_func'):
            if callable(getattr(self, 'cell_func')):
                if (((getattr(self, 'cell_func').__code__.co_varnames)[:3]) != ('_', 'cell', 'env')):
                    raise AttributeError(f"Cellrule class env_rule method arguments must begin with {('_', 'cell', 'env')}.")
            else:
                raise AttributeError(f"Cellrule class must have 'env_rule' method.")
        else:
            raise AttributeError(f"Cellrule class must have 'env_rule' method.")


    def update_sensors(self, new_sensors):
        self.sensors = np.array(new_sensors)
        
    def update_defaults(self):
        pass
    
class EnvRule:
    def __init__(self):
        if hasattr(self,'display_name') and hasattr(self,'exp') and  hasattr(self,'params_dict'):
            self._cell_rule_first = True
            self.__class__.params = {key: self.params_dict[key]["val"] for key in self.params_dict.keys()}
            self.__class__.params_exp = {key: self.params_dict[key]["exp"] for key in self.params_dict.keys()}
            self.check_env_function()
        else:
            raise AttributeError(f"Envrule class must have the following attributes {['display_name', 'exp', 'params_dict']} set in its init function.")
    
    def check_env_function(self):
        if hasattr(self, 'env_func'):
            if callable(getattr(self, 'env_func')):
                if (((getattr(self, 'env_func').__code__.co_varnames)[:2]) != ('_', 'env')):
                    raise AttributeError(f"Envrule class env_rule method arguments must begin with {('_', 'env')}.")
            else:
                raise AttributeError(f"Envrule class must have 'env_rule' method.")
        else:
            raise AttributeError(f"Envrule class must have 'env_rule' method.")

    def update_defaults(self):
        pass
    
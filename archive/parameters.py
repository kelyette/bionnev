import yaml, numpy as np

class Params:
    def __init__(self):
        with open("parameters/config.yaml", "r") as f:
            config = yaml.safe_load(f)

        with open("parameters/params.yaml", "r") as f:
            all_params = yaml.safe_load(f)
            params = all_params['values']
            params_exp = all_params['exp']

        with open("parameters/cfg_env_rules.yaml", "r") as f:
            env_rules = yaml.safe_load(f)
        default_env_rule_key = config['default_env_rule']
        default_env_rule = env_rules[default_env_rule_key]['fun']

        with open("parameters/cfg_cell_rules.yaml", "r") as f:
            cell_rules = yaml.safe_load(f)
        default_cell_rule_key = config['default_cell_rule']
        default_cell_rule = cell_rules[default_cell_rule_key]['fun']

        params['num_sensors'] = cell_rules[default_cell_rule_key]['num_sensors']
        params['num_actions'] = cell_rules[default_cell_rule_key]['num_actions']
        
        self.list = params
        self.get_mean_std()
        self.exp = params_exp
        self.env_rules_dict = env_rules 
        self.env_rule_key = default_env_rule_key
        self.env_rule = default_env_rule
        self.cell_rules_dict = cell_rules
        self.cell_rule_key = default_cell_rule_key
        self.cell_rule = default_cell_rule

        self.colors = np.array([
            [255, 255, 255], # WHITE
            [164, 55, 72],   # RED
            [174, 117, 58],  # YELLOW
            [39, 93, 108],   # BLUE
            [76, 148, 50],   # GREEN
        ])

    def get_mean_std(self):
        self.list["mean_physics"] = np.array([
            self.list["mean_death"],
            self.list["mean_sex"],
            self.list["mean_strength"],
            self.list["mean_velocity"],
        ])

        self.list["std_physics"] = np.array([
            self.list["std_death"],
            self.list["std_sex"],
            self.list["std_strength"],    
            self.list["std_velocity"],    
        ])


    def update_params(self, new_params):
        self.list = new_params 
    
    def update_key(self, new_env_rule=None, new_cell_rule=None):
        if new_env_rule:
            self.env_rule_key = self.env_rules_dict.keys()[self.env_rules_dict.values().index(new_env_rule)]
        if new_cell_rule:
            self.cell_rule_key = self.cell_rules_dict.keys()[self.cell_rules_dict.values().index(new_cell_rule)]

    def update_env_rule(self, new_env_rule):
        self.env_rule = new_env_rule
        self.env_rule_key = self.update_key(new_env_rule)
        
    def update_cell_rule(self, new_cell_rule):
        self.cell_rule = new_cell_rule
        self.cell_rule_key = self.update_key(new_cell_rule)
        self.list['num_sensors'] = self.cell_rules_dict[self.cell_rule_key]['num_sensors']
        self.list['num_actions'] = self.cell_rules_dict[self.cell_rule_key]['num_actions']

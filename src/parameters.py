class Params:
    def __init__(self, params, env_rule_dict, env_rule, cell_rule_dict, cell_rule):
        self.list = params
        self.env_rule_dict = env_rule_dict 
        self.env_rule = env_rule
        self.cell_rule_dict = cell_rule_dict
        self.cell_rule = cell_rule

    def update_params(self, new_params):
        self.list = new_params 

    def update_env_rule(self, new_env_rule):
        self.env_rule = new_env_rule
        
    def update_cell_rule(self, new_cell_rule):
        self.cell_rule = new_cell_rule
        self.list

import numpy as np
from src.rules.rule_classes import CellRule

class Rule1(CellRule):
    def __init__(self):
        super().__init__()
        self.display_name = "Rule1"
        self.exp = "The cells have no changing parameters. They only have a constant input of 1. Their actions is to either move left, right, north or south."    
        self.num_sensors = 1
        self.num_actions = 4
        self.params_dict = {
            "mean_death": {"val": 20, "exp": "Mean death age (one unit of age is one simulation days)."},
            "std_death": {"val": 5, "exp": "Standard deviation of age."},
            "mean_velocity": {"val": 1, "exp": "Mean velocity of the cell. This represents the number of pixels the cell will move if it has a moving signal."},
            "std_velocity": {"val": 0.3, "exp": "Standard deviaiton of the velocity of the cells."},
        }
        self.params = {key: self.params_dict[key]["val"] for key in self.params_dict.keys()}
        self.exp = {key: self.params_dict[key]["exp"] for key in self.params_dict.keys()}
        
        self.params['mean_physics'] = np.array([
            self.params['mean_death'],
            self.params['mean_velocity'],
        ])
        
        self.params['std_physics'] = np.array([
            self.params['std_death'],
            self.params['std_velocity'],
        ])
    
    def cell_func(_, self):
        move = (self.actions[:2].ravel() - self.actions[2:4].ravel()) * self.velocity
        self.pos += move - (move + self.pos > (self.grid_size-1)) * 2*((move + self.pos) - self.grid_size+1) - (move + self.pos < 0) * 2*((move + self.pos))
        
        self.sensors = np.array([
            1,
        ])
        
        self.think()
        self.live() 

def cell_rule2(self, clock, pos_map):
    move = (self.actions[:2].ravel() - self.actions[2:4].ravel()) * self.velocity
    self.pos += move - (move + self.pos > (self.grid_size-1)) * 2*((move + self.pos) - self.grid_size+1) - (move + self.pos < 0) * 2*((move + self.pos))
    
    self.sensors = np.array([
        1,
        np.random.random(1).item(),
        np.random.uniform(1),
        int(self.pos[0] / self.grid_size),
        int(self.pos[1] / self.grid_size),
    ])
    self.think()
    self.live()    


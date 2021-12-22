import numpy as np
from src.rule_classes import CellRule

class Rule0(CellRule):
    def __init__(self):
        self.display_name = "Constant Move"
        self.exp = "The cells have no changing parameters. They only have a constant input of 1. Their actions is to either move left, right, north or south."    
        self.phys_attr = ['death','velocity']
        self.params_dict = {
            "mean_death": {"val": 25, "exp": "Mean death age (one unit of age is one simulation days)."},
            "std_death": {"val": 5, "exp": "Standard deviation of age."},
            "mean_velocity": {"val": 1, "exp": "Mean velocity of the cell. This represents the number of pixels the cell will move if it has a moving signal."},
            "std_velocity": {"val": 0.3, "exp": "Standard deviaiton of the velocity of the cells."},
        }
        self.num_sensors = 1
        self.num_actions = 4
        super().__init__()
    
    def cell_func(_, cell, env):
        move = np.rint((cell.actions[:2].ravel() - cell.actions[2:4].ravel()) * cell.velocity)
        cell.pos += move - (move + cell.pos > (env.grid_size-1)) * 2*((move + cell.pos) - env.grid_size+1) - (move + cell.pos < 0) * 2*((move + cell.pos))
        
        cell.sensors = np.array([
            1.0,
        ])

        cell.think()
        cell.live() 

class Rule1(CellRule):
    def __init__(self):
        self.display_name = "Changing Move"
        self.exp = "The cells have the following parameters: 1 (constant). They only have a constant input of 1. Their actions is to either move left, right, north or south."    
        self.phys_attr = ['death','velocity']
        self.params_dict = {
            "mean_death": {"val": 25, "exp": "Mean death age (one unit of age is one simulation days)."},
            "std_death": {"val": 5, "exp": "Standard deviation of age."},
            "mean_velocity": {"val": 1, "exp": "Mean velocity of the cell. This represents the number of pixels the cell will move if it has a moving signal."},
            "std_velocity": {"val": 0.3, "exp": "Standard deviaiton of the velocity of the cells."},
            "osc_cycle": {"val": 0.3, "exp": "Number of time frames for a full oscillatory cycle"}
        }
        self.num_sensors = 5
        self.num_actions = 4

        super().__init__()
    
    def cell_func(_, cell, env):
        move = np.rint((cell.actions[:2].ravel() - cell.actions[2:4].ravel()) * cell.velocity)
        cell.pos += move - (move + cell.pos > (env.grid_size-1)) * 2*((move + cell.pos) - env.grid_size+1) - (move + cell.pos < 0) * 2*((move + cell.pos))
        
        cell.sensors = np.array([
            1.0,
            np.random.random(1).item(),
            np.sin(2* np.pi * env.clock/cell.osc_cycle).item(),
            cell.pos[0] / env.grid_size,
            cell.pos[1] / env.grid_size,
        ])
        
        cell.think()
        cell.live()

class Rule2(CellRule):
    def __init__(self):
        self.display_name = 'Rule3'
        self.exp = ''
        self.phys_attr = ['death']
        self.params_dict = {
            "mean_death": {"val": 50, "exp": "Mean death age (one unit of age is one simulation days)."},
            "std_death": {"val": 2, "exp": "Standard deviation of age."},
            'strength': {'val': 0, 'exp': 'Initial strength'}
        }
        self.num_sensors = 1
        self.num_actions = 4
        
        super().__init__()
        
    def cell_func(_, cell, env):
        move = np.rint(cell.actions[:2].ravel() - cell.actions[2:4].ravel())
        last_pos = cell.pos.copy()
        cell.pos += move - (move + cell.pos > (env.grid_size-1)) * 2*((move + cell.pos) - env.grid_size+1) - (move + cell.pos < 0) * 2*((move + cell.pos))
        
        if (cell.pos != last_pos).any():
            cell.strength += 1
        
        cell.sensors = np.array([
            1.0
        ])
        
        cell.think()
        cell.live()
        
class Rule3(CellRule):
    def __init__(self):
        self.display_name = 'Rule3'
        self.exp = ''
        self.phys_attr = ['death']
        self.params_dict = {
            "mean_death": {"val": 50, "exp": "Mean death age (one unit of age is one simulation days)."},
            "std_death": {"val": 2, "exp": "Standard deviation of age."},
        }
        self.num_sensors = 4
        self.num_actions = 4
        
        super().__init__()
    
    def cell_func(_, cell, env):
        move = np.rint(cell.actions[:2].ravel() - cell.actions[2:4].ravel())
        cell.pos += move - (move + cell.pos > (env.grid_size-1)) * 2*((move + cell.pos) - env.grid_size+1) - (move + cell.pos < 0) * 2*((move + cell.pos))
        
        cell.neighbors = sum(env.get_interacting_cells(cell=cell, xradius=(1, 1), yradius=(1, 1)).flatten())
        cell.neighbors_top = sum(env.get_interacting_cells(cell=cell, xradius=(0, 0), yradius=(2, 0)).flatten())
        cell.neighbors_right = sum(env.get_interacting_cells(cell=cell, xradius=(0, 2), yradius=(0, 0)).flatten())
        cell.neighbors_bottom = sum(env.get_interacting_cells(cell=cell, xradius=(0, 0), yradius=(0, 2)).flatten())
        cell.neighbors_left = sum(env.get_interacting_cells(cell=cell, xradius=(2, 0), yradius=(0, 0)).flatten())
        
        cell.sensors = np.array([
            cell.neighbors_top,
            cell.neighbors_left,
            cell.neighbors_bottom,
            cell.neighbors_right,
        ])
        
        cell.think()
        cell.live()
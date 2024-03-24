import numpy as np
from classes.rule_classes import CellRule
import torch

import matplotlib.pyplot as plt

class Rule0(CellRule):
    def __init__(self):
        self.display_name = "Constant Move"
        self.exp = "The cells have no changing parameters. They only have a constant input of 1. Their actions is to either move left, right, north or south."    
        self.phys_attr = ['death','velocity']
        self.params_dict = {
            "mean_death": {"val": 25, "exp": "Mean death age (one unit of age is one simulation days)."},
            "std_death": {"val": 5, "exp": "Standard deviation of age."}
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

        cell.step()
        cell.live() 

class Rule1(CellRule):
    def __init__(self):
        self.display_name = "Changing Move"
        self.exp = "The cells have the following parameters: 1 (constant). They only have a constant input of 1. Their actions is to either move left, right, north or south."    
        self.phys_attr = ['death','velocity']
        self.params_dict = {
            "mean_death": {"val": 400, "exp": "Mean death age (one unit of age is one simulation days)."},
            "std_death": {"val": 25, "exp": "Standard deviation of age."},
            "mean_velocity": {"val": 1, "exp": "Mean velocity of the cell. This represents the number of pixels the cell will move if it has a moving signal."},
            "std_velocity": {"val": 0.3, "exp": "Standard deviaiton of the velocity of the cells."},
            "osc_cycle": {"val": 0.3, "exp": "Number of time frames for a full oscillatory cycle"}
        }
        self.num_sensors = 5
        self.num_actions = 4

        super().__init__()
    
    def cell_func(_, cell, env):
        toplot = cell.actions[0].ravel()[0].item()
        if toplot and env.clock % 25 == 0:
            env.x.append(toplot)

        if env.clock == 200:
            exit()

        move = np.rint((cell.actions[:2].ravel() - cell.actions[2:4].ravel()) * cell.velocity)
        cell.pos += move - (move + cell.pos > (env.grid_size-1)) * 2*((move + cell.pos) - env.grid_size+1) - (move + cell.pos < 0) * 2*((move + cell.pos))
        
        cell.sensors = np.array([
            1.0,
            np.random.random(1).item(),
            np.sin(2* np.pi * env.clock/cell.osc_cycle).item(),
            cell.pos[0] / env.grid_size,
            cell.pos[1] / env.grid_size,
        ])
        
        cell.step()
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
        
        cell.step()
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
        
        cell.step()
        cell.live()

class Rule4(CellRule):
    def __init__(self):
        self.display_name = "Social instinct"
        self.exp = """The cells need to be close to each other, but not too
                      close, to reproduce.  move based on their
                      velocity, itself based on their acceleration, itself
                      based on the average vector between the neighboring
                      cells. The goal is to replicate a flocking behavior.
                      (use env rule 5)
        """
        self.phys_attr = ['death']
        self.params_dict = {
            "mean_death": {"val": 25, "exp": "Mean death age (one unit of age is one simulation days)."},
            "std_death": {"val": 5, "exp": "Standard deviation of age."},
        }
        self.num_sensors = 1
        self.num_actions = 2
        
        super().__init__()
    
    def cell_func(_, cell, env):
        cell.acc = np.zeros(2, dtype=float)
        move = np.rint((cell.actions[:2].ravel() - cell.actions.ravel()) * cell.vel)
        if (cell.id == 1): print(cell.actions[:2], cell.actions)
        cell.acc = np.random.random(2) * 2 - 1

        cell.pos += cell.vel / 2
        cell.vel += cell.acc

        cell.pos = np.floor(cell.pos)
        
        """ neighbors = env.get_neighbors(cell, 1) """
        
        cell.sensors = np.array([
            1.0,
        ])

        cell.step()
        cell.live()

class Rule5(CellRule):
    def __init__(self):
        self.display_name = "Flocking"
        self.exp = """The cells move based on their velocity, itself based on
                      their acceleration, itself based on the average vector
                      of the neighboring cells. The goal is to replicate a
                      flocking behavior by favoring the reproduciton of cells
                      that are close to each other in the env rule.
                      (use env rule 5)
        """
        self.phys_attr = ['death']
        self.params_dict = {
            "mean_death": {"val": 100, "exp": "Mean age of death."},
            "std_death": {"val": 25, "exp": "Standard deviation of age of death."},
            "osc_cycle": {"val": 2, "exp": "Number of time frames for a full oscillatory cycle"},
            "req_neighbor_distance": {"val": 5, "exp": "Distance to the closest neighbor"},
            "neighbor_radius": {"val": 10, "exp": "Radius around the cell to look for neighbors"},
            "safe_frame_count": {"val": 0, "exp": "Number of consecutive frames a cell has been safe"},
            "n_neighbors": {"val": 0, "exp": "Current amount of neighbors"}
        }
        self.num_sensors = 2
        self.num_actions = 2
        self.hidden_shape = [6, ]
        super().__init__()
    
    def cell_func(_, cell, env):
        vel = cell.actions[:2].ravel() 
        cell.pos += 3 * vel - 1.5
        cell.pos = np.clip(cell.pos, 0, env.grid_size)

        neighbors = env.get_neighbors(cell, cell.req_neighbor_distance) # TODO optimize
        cm_diff = np.zeros(2)
        if neighbors:
            neighbors_cm = np.mean([c.pos for c in neighbors], axis=0)
            cm_diff = cell.pos - neighbors_cm

        cell.neighbors = len(neighbors)

        cell.sensors = torch.tensor([
            cm_diff[0],
            cm_diff[1]
        ], dtype=torch.float32)

        cell.step()
        cell.live()
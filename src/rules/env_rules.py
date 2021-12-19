import numpy as np
from src.cell import Cell
from src.rules.rule_classes import EnvRule

class Rule1(EnvRule):
    def __init__(self):
        self.display_name = "Simple rectangle"
        self.exp = "The cells each reproduce one new cell if they are a subrectangle of the grid (can be chosen to be any). The new cell inherit the exact same brain_dna. Every new cell is then randomly put in the grid."    
        self.params_dict = {
            "grid_size": {"val": 30, "exp": "Grid size."},
            "num_cells": {"val": 10, "exp": "Number of initial cells."},
            "regeneration_days": {"val": 10, "exp": "Frequency (in days) at which the cells reproduce."},
            "percent_grid": {"val": 0.4, "exp": "Number of."},
            "horizontal": {"val": 0, "exp": "Variable that dicates if the zone is divided through an horizontal (1) or vertical(0) line."},
            "bottom": {"val": -1, "exp": "Variables that dictates if the zone is for the min of the coordinate (-1) or max(1)"},
        }
        super().__init__()
    def env_func(_, env):
        reproduceable_cells = [cell for cell in env.cells if env.params['bottom']* cell.pos[env.params['horizontal']] >= env.params['bottom'] *int((env.grid_size-1)*env.params['percent_grid'])]
        for cell in env.cells:
            cell.reproduceable = True if cell in reproduceable_cells else False

        if env.clock % env.params['regeneration_days'] == 0: 
            new_cells = [Cell(env.envrule, env.cellrule) for i in range(len(reproduceable_cells))]
            for i,c in enumerate(new_cells):
                c.pos = np.random.uniform(0, env.grid_size-1,2) 
                c.brain_dna = reproduceable_cells[i].brain_dna 
            env.cells.extend(new_cells) 


class Rule2(EnvRule):
    def __init__(self):
        self.display_name = "Rule2"
        self.exp = "The cells each reproduce one new cell if they are in a specific corner of the grid. Every new cell is then randomly put in the grid ."    
        self.params_dict = {
            "grid_size": {"val": 30, "exp": "Grid size."},
            "num_cells": {"val": 10, "exp": "Number of initial cells."},
            "regeneration_days": {"val": 10, "exp": "Frequency (in days) at which the cells reproduce."},
            "percent_grid": {"val": 0.4, "exp": "Number of."},
            "horizontal": {"val": 0, "exp": "Variable that dicates if the zone is divided through an horizontal (1) or vertical(0) line."},
            "bottom": {"val": -1, "exp": "Variables that dictates if the zone is for the min of the coordinate (-1) or max(1)"},
        }
        super().__init__()

    def env_func(_, env):
        reproduceable_cells = [cell for cell in env.cells if env.params['bottom'] * cell.pos[env.params['horizontal']] >= env.params['bottom'] *int((env.grid_size-1)*env.params['percent_grid'])]
        for cell in env.cells:
            cell.reproduceable = True if cell in reproduceable_cells else False

        if env.clock % env.params['regeneration_days'] == 0: 
            new_cells = [Cell(env.envrule, env.cellrule) for i in range(len(reproduceable_cells))]
            for i,c in enumerate(new_cells):
                c.pos = np.random.uniform(0, env.size-1,2) 
                c.brain_dna = reproduceable_cells[i].brain_dna 
            env.cells.extend(new_cells) 
        return 1
import numpy as np
from src.cell import Cell
from src.rules.rule_classes import EnvRule

class Rule1(EnvRule):
    def __init__(self):
        super().__init__()
        self.display_name = "Rule1"
        self.exp = "The cells each reproduce one new cell if they are in the bottom half of the grid. Every cell is then randomly put in the grid (even the already existing ones)."    
        self.params_dict = {
            "grid_size": {"val": 30, "exp": "Grid size."},
            "num_cells": {"val": 500, "exp": "Number of initial cells."},
            "regeneration_days": {"val": 20, "exp": "Frequency (in days) at which the cells reproduce."}
        }
        self.params = {key: self.params_dict[key]["val"] for key in self.params_dict.keys()}
        self.exp = {key: self.params_dict[key]["exp"] for key in self.params_dict.keys()}
        
    def env_func(self):
        if self.clock % self.params.list['regeneration_days'] == 0: 
            reproduceable_cells = [cell for cell in self.cells if cell.pos[0] >= int((self.size -1)/4)]
            self.spawn_cells(reproduceable_cells)
            for cell in self.cells:
                cell.pos = np.random.uniform(0, self.size-1,2)  
        return 1

class Rule2(EnvRule):
    def __init__(self):
        super().__init__()
        self.display_name = "Rule1"
        self.exp = "The cells each reproduce one new cell if they are in the bottom half of the grid. Every cell is then randomly put in the grid (even the already existing ones)."    
        self.params = {
            "regeneration_days": []
        }
        
    def env_func(self):
        reproduceable_cells = [cell for cell in self.cells if cell.pos[0] >= int(2*(self.size -1)/3)]
        for cell in self.cells:
            cell.reproduceable = True if cell in reproduceable_cells else False
        if self.clock % self.params.list['regeneration_days'] == 0: 
            new_cells = [Cell(self.params) for i in range(len(reproduceable_cells))]
            for i,c in enumerate(new_cells):
                setattr(c, self.cellrule[0], self.cellrule[1])
                c.cellrule = self.cellrule
                c.pos = np.random.uniform(0, self.size-1,2) 
                c.brain_dna = reproduceable_cells[i].brain_dna 
            self.cells.extend(new_cells) 
        return 1

def env_rule3(self):
    reproduceable_cells = [cell for cell in self.cells if sum((cell.pos-int((self.size -1)/2))**2)<12**2]
    for cell in self.cells:
        cell.reproduceable = True if cell in reproduceable_cells else False
    if self.clock % self.params.list['regeneration_days'] == 0: 
        new_cells = [Cell(self.params) for i in range(len(reproduceable_cells))]
        for i,c in enumerate(new_cells):
            setattr(c, self.cellrule[0], self.cellrule[1])
            c.cellrule = self.cellrule
            c.pos = np.random.uniform(0, self.size-1,2) 
            c.brain_dna = reproduceable_cells[i].brain_dna 
        self.cells.extend(new_cells) 
    self.cells = [c for c in self.cells if c.alive]
    return 1    

def env_rule4(self):
    if not np.any(self.cells):
        return 0
    self.clock += 1   
    self.call_all(self.cells, self.cellrule[0], self.clock, self.pos_map)
    reproduceable_cells = [cell for cell in self.cells if (sum(cell.pos)  < int(self.size/1.5))]
    for cell in self.cells:
        cell.reproduceable = True if cell in reproduceable_cells else False
    if self.clock % self.params.list['regeneration_days'] == 0: 
        new_cells = [Cell(self.params) for i in range(len(reproduceable_cells))]
        for i,c in enumerate(new_cells):
            setattr(c, self.cellrule[0], self.cellrule[1])
            c.cellrule = self.cellrule
            c.pos = np.random.uniform(0, self.size-1,2) 
            c.brain_dna = reproduceable_cells[i].brain_dna 
        self.cells.extend(new_cells) 
    self.cells = [c for c in self.cells if c.alive]
    return 1 
import numpy as np
from classes.cell import Cell

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from parameters.env_rules import EnvRule
    from parameters.cell_rules import CellRule

# environment class
# holds every cell and handles each step
class Environment:
    def __init__(self, envrule: 'EnvRule', cellrule: 'CellRule'):
        self.envrule = envrule
        self.cellrule = cellrule
        self.params = envrule.params
        self.clock = 0
        self.grid_size = self.params["grid_size"]
        self.num_cells = self.params["num_cells"]
        # initialize the grid
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)

        # intiialize the cells
        self.cells = self.create_cells(self.num_cells)
        self.pos_map = 0
    
    def create_cells(self, num_cells: int):
        cell_attributes = {}
        if hasattr(self.envrule, 'cell_attributes'):
            cell_attributes = {k: v['initial_val'] for k, v in self.envrule.cell_attributes.items()}

        return [Cell(self.envrule, self.cellrule, i, **cell_attributes) for i in range(num_cells)]
    
    def add_cells(self, new_cells: list, reproduceable_cells: list | None = None):
        if reproduceable_cells:
            for i, c in enumerate(new_cells):
                c.pos = np.random.uniform(0, self.grid_size, 2)
                c.brain_dna = reproduceable_cells[i].brain_dna

        self.cells.extend(new_cells)

    # calls the rule function of each cell
    def call_cell_rules(self, *args, **kwargs):
        for cell in self.cells:
            cell.rule.cell_func(cell, self,  *args, **kwargs)

    def get_state(self):
        return [cell.get_state() for cell in self.cells]
    
    def get_neighbors(self, cell, radius=3): # get all the neighbors of a cell in the radius of a specific cell
        cells = self.cells
        neighbors = []
        for c in cells:
            if c != cell:
                if np.sqrt((c.pos[0] - cell.pos[0])**2 + (c.pos[1] - cell.pos[1])**2) < radius:
                    neighbors.append(c)
        
        return neighbors
    
    def next(self):
        if not np.any(self.cells):
            return 0
        self.clock += 1
        
        if self.envrule._cell_rule_first:
            self.call_cell_rules()
            self.cells = [c for c in self.cells if c.alive]
            if len(self.cells) < 10:
                new_cells = self.create_cells(self.envrule.params["num_cells"])
                self.add_cells(new_cells)
            self.envrule.env_func(self)
            
        else:
            self.envrule.env_func(self)            
            self.call_cell_rules()
            self.cells = [c for c in self.cells if c.alive]
            if len(self.cells) < 10:
                new_cells = self.create_cells(self.envrule.params["num_cells"])
                self.add_cells(new_cells)
        
        return 1
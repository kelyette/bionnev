import numpy as np
from src.cell import Cell

class Environment:
    def __init__(self, envrule, cellrule):
        self.envrule = envrule
        self.cellrule = cellrule
        self.params = envrule.params
        self.clock = 0
        self.grid_size = self.params["grid_size"]
        self.num_cells = self.params["num_cells"]
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.cells = [Cell(self.envrule, self.cellrule) for _ in range(self.num_cells)]
        self.pos_map = 0
        
    def call_cell_rules(self, *args, **kwargs):
        for cell in self.cells:
            cell.rule.cell_func(cell, self,  *args, **kwargs)

    def get_grid(self, plot):
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        
        for rule in plot.rules:
            self.add_type(**rule)
            
        return plot.colors[self.grid.copy()]
    
    def add_type(self, show_cond, cell_cond, color_num):
        if show_cond(self):
            pos_map = list(map(lambda cell: [int(cell.pos[0]), int(cell.pos[1])], (cell for cell in self.cells if cell_cond(cell))))
            
            if pos_map:
                rows, cols = zip(*pos_map)
                self.grid[rows, cols] = color_num

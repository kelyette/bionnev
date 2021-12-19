import numpy as np
from src.cell import Cell

class Environment:
    def __init__(self, envrule, cellrule):
        self.envrule = envrule
        self.cellrule = cellrule
        self.params = envrule.params
        self.clock = 0
        self.size = self.params["grid_size"]
        self.num_cells = self.params["num_cells"]
        self.grid = np.zeros((self.size, self.size), dtype=int)
        self.cells = [Cell(self.envrule, self.cellrule) for _ in range(self.num_cells)]
        self.pos_map = 0
        
    def call_cell_rules(self, *args, **kwargs):
        for cell in self.cells:
            cell.rule.cell_func(cell, *args, **kwargs)

    def get_grid(self, colors):
        self.grid = np.zeros((self.size, self.size), dtype=int)
        self.add_type(True, lambda cell: not cell.reproduceable, 2)
        self.add_type(True, lambda cell: cell.reproduceable, 4)
        self.add_type(self.clock>5, lambda cell: cell.age<=5, 1)
        return colors[self.grid.copy()]
    
    def add_type(self, show_cond, cell_cond, color):
        if show_cond:
            pos_map = list(map(lambda cell: [int(cell.pos[0]), int(cell.pos[1])], (cell for cell in self.cells if cell_cond(cell))))
            if pos_map:
                rows, cols = zip(*pos_map)
                self.grid[rows, cols] = color
        
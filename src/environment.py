import numpy as np
from src.cell import Cell

class Environment:
    def __init__(self, envrule, cellrule):
        self.params = envrule.params
        self.clock = 0
        self.size = self.params["grid_size"]
        self.num_cells = self.params["num_cells"]
        self.grid = np.zeros((self.size, self.size), dtype=int)
        self.cells = [Cell(envrule, cellrule) for _ in range(self.num_cells)]
        self.pos_map = 0
        
    def call_all(self, chosen_cells, attr, *args, **kwargs):
        for cell in chosen_cells:
            getattr(cell.rule, attr)(cell, *args, **kwargs)

    def get_grid(self):
        self.grid = np.zeros((self.size, self.size), dtype=int)
        self.pos_map = list(map(lambda cell: [int(cell.pos[0]), int(cell.pos[1])], (cell for cell in self.cells if not cell.reproduceable)))
        rows, cols = zip(*self.pos_map)
        self.grid[rows, cols] = 4
        
        self.pos_map = list(map(lambda cell: [int(cell.pos[0]), int(cell.pos[1])], (cell for cell in self.cells if cell.reproduceable)))
        if self.pos_map:
            rows, cols = zip(*self.pos_map)
            self.grid[rows, cols] = 2

        if self.clock > 5:    
            self.pos_map = list(map(lambda cell: [int(cell.pos[0]), int(cell.pos[1])], (cell for cell in self.cells if cell.age <= 5)))
            if self.pos_map:
                rows, cols = zip(*self.pos_map)
                self.grid[rows, cols] = 1
            
        return self.params.colors[self.grid].copy()
    
    def add_type(self, show_cond, cell_cond, color):
        if show_cond:
            pos_map = list(map(lambda cell: [int(cell.pos[0]), int(cell.pos[1])], (cell for cell in self.cells if cell_cond(cell))))
            if pos_map:
                rows, cols = zip(*pos_map)
                self.grid[rows, cols] = color
        
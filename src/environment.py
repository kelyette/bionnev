import numpy as np
from src.cell import Cell

class Environment:
    def __init__(self,params):
        self.params = params
        self.clock = 0
        self.size = int(params["grid_size"])
        self.ncell = params["n_cell"]
        self.grid = np.zeros((self.size, self.size), dtype=int)
        self.cells = [Cell(params) for _ in range(int(params["n_cell"]))]
        self.pos_map = 0
        
    def call_all(self, chosen_cells, attr, *args, **kwargs):
        for cell in chosen_cells:
            try:
                getattr(cell, attr)(cell, *args, **kwargs)
            except Exception as e:
                print(e)

    def get_grid(self):
        self.grid = np.zeros((self.size, self.size), dtype=int)
        self.pos_map = list(map(lambda cell: [int(cell.pos[0]), int(cell.pos[1])], self.cells))
        rows, cols = zip(*self.pos_map)
        self.grid[rows, cols] = 1
        return self.grid.copy()
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
            pos_map = self.get_pos_map(cell_cond)
            if pos_map:
                rows, cols = zip(*pos_map)
                self.grid[rows, cols] = color_num

    def get_pos_map(self, cond=True, bind_cell=False):
        cond = lambda _: True if cond == True else cond
        if not bind_cell:
            pos_map = list(map(lambda cell: [int(cell.pos[0]), int(cell.pos[1])], (cell for cell in self.cells if cond(cell))))
        else:
            pos_map = list(map(lambda cell: [cell, [int(cell.pos[0]), int(cell.pos[1])]], (cell for cell in self.cells if cond(cell))))
   
        return pos_map
    
    def get_interacting_cells(self, cond=True, radius=0):
        pos_map = self.get_pos_map(cond,bind_cell=True)
        clusters = []
        for cell1 in pos_map:
            for cell2 in pos_map:
                if (cell1 is not cell2) and sum([(cell1[1][i]-cell2[1][i])**2 for i in (0,1)])<radius:
                    clusters.append([cell1[0], cell2[0]])

    def next(self, *args, **kwargs):
        if not np.any(self.cells):
            return 0
        self.clock += 1 
        if self.envrule.__cell_rule_first:
            self.call_cell_rules()
            self.cells = [c for c in self.cells if c.alive]
            self.envrule.env_func(self, *args, **kwargs)
            
        else:
            self.envrule.env_func(self,  *args, **kwargs)            
            self.call_cell_rules()
            self.cells = [c for c in self.cells if c.alive]
        
        return 1
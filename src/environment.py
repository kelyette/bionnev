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

    def get_grid(self, plot=None, stack=''):
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        
        if stack == 'add':
            height_grid = self.grid.copy()
            
            pos_map = self.get_pos_map(cell_cond=True)
            for y in range(self.grid_size - 1):
                for x in range(self.grid_size - 1):
                    if [x, y] in pos_map:
                        height_grid[x, y] += 1
                        
            return height_grid
                
        
        for rule in plot.rules:
            self.add_type(**rule)
            
        return plot.colors[self.grid.copy()]
    
    def add_type(self, show_cond, cell_cond, color_num):
        if isinstance(show_cond, bool):
            show_cond = lambda _: show_cond
        if show_cond(self):
            pos_map = self.get_pos_map(cell_cond=cell_cond, remove_duplicates=True)
            if pos_map:
                rows, cols = zip(*pos_map)
                self.grid[rows, cols] = color_num

    def get_pos_map(self, cell_cond=True, bind_cell=False, remove_duplicates=False):
        if isinstance(cell_cond, bool):
            cell_cond = lambda _ : cell_cond
        if bind_cell:
            pos_map = list(map(lambda cell: [cell, [int(cell.pos[0]), int(cell.pos[1])]], (cell for cell in self.cells if cell_cond(cell))))
        else:
            pos_map = list(map(lambda cell: [int(cell.pos[0]), int(cell.pos[1])], (cell for cell in self.cells if cell_cond(cell))))
   
            np_pos_map = np.array(pos_map)
            np_pos_map_wo_dupe = np.unique(np_pos_map, axis=0)
            pos_map_wo_dupe = list(map(lambda array: list(array), np_pos_map_wo_dupe))
            
            if remove_duplicates:
                return pos_map_wo_dupe

        return pos_map
    
    def get_interacting_cells(self, cell=False, cond=True, flat=False, xradius=(0, 0), yradius=(0, 0)):
        pos_map = self.get_pos_map(cond, bind_cell=True)
        height_grid = self.get_grid(stack='add')
        
        if cell:
            return height_grid[int(cell.pos[0]-xradius[0]):int(cell.pos[0]+xradius[1]+1), int(cell.pos[1]-yradius[0]):int(cell.pos[1]+yradius[1]+1)]
        
        else:
            return [height_grid[cell[1][0]-xradius[0]:cell[1][0]+xradius[1]+1, cell[1][1]-yradius[0]:cell[1][1]+yradius[1]+1] for cell in pos_map]           
        
    def next(self, *args, **kwargs):
        if not np.any(self.cells):
            return 0
        self.clock += 1
        
        if self.envrule._cell_rule_first:
            self.call_cell_rules()
            self.cells = [c for c in self.cells if c.alive]
            self.envrule.env_func(self)
            
        else:
            env_func_args = (self, )
            self.envrule.env_func(self)            
            self.call_cell_rules()
            self.cells = [c for c in self.cells if c.alive]
        
        return 1
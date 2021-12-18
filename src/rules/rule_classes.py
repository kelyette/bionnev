import numpy as np
from src.cell import Cell

class CellRule:
    def __init__(self):
        pass
    
    def update_sensors(self, new_sensors):
        self.sensors = np.array(new_sensors)
        
    def update_defaults(self):
        pass
    
class EnvRule:
    def __init__(self):
        self.__cell_rule_first = True
        
    def update_defaults(self):
        pass
    
    def next(self, *args, **kwargs):
        if not np.any(self.cells):
            return 0
        
        self.clock += 1 
        if self.__cell_rule_first:
            # self.call_all(self.cells, self.cellrule[0])
            self.cells = [c for c in self.cells if c.alive]
            self.env_func(*args, **kwargs)
            
        else:
            self.env_func()            
            # self.call_all(self.cells, self.cellrule[0], self.clock, self.pos_map)
            self.cells = [c for c in self.cells if c.alive]
        
        
        return 1
        
    # def spawn_cells(self, parent_cells, mapping):
    #     new_cells = [Cell(self.params) for i in range(len(parent_cells))]
    #     for i, c in enumerate(new_cells): 
    #         setattr(c, self.cellrule[0], self.cellrule[1])
    #         c.cellrule = self.cellrule
            
    #         for m in mapping.keys():
    #             setattr(c, m, mapping[m](i))
                
    #     self.cells.extend(new_cells)
        # mapping = {'brain_dna': lambda i: i }
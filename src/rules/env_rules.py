import numpy as np
from src.cell import Cell

def env_rule1(self):
    if not np.any(self.cells):
        return 0
    self.clock += 1   
    self.call_all(self.cells, self.cellrule[0], self.clock, self.pos_map)

    if self.clock % 100 == 0: 
        reproduceable_cells = [cell for cell in self.cells if cell.pos[0] >= int((self.size -1)/4)]
        new_cells = [Cell(self.params) for i in range(len(reproduceable_cells))]
        for c in new_cells:
            setattr(c, self.cellrule[0], self.cellrule[1])
            c.cellrule = self.cellrule
        self.cells.extend(new_cells)
        for cell in self.cells:
            cell.pos = np.random.uniform(0, self.size-1,2)  
    self.cells = [c for c in self.cells if c.alive]
    return 1

def env_rule2(self):
    if not np.any(self.cells):
        return 0
    self.clock += 1   
    self.call_all(self.cells, self.cellrule[0], self.clock, self.pos_map)

    if self.clock % self.params['regeneration_days'] == 0: 
        reproduceable_cells = [cell for cell in self.cells if cell.pos[0] >= int((self.size -1)/4)]
        new_cells = [Cell(self.params) for i in range(len(reproduceable_cells))]
        for i,c in enumerate(new_cells):
            setattr(c, self.cellrule[0], self.cellrule[1])
            c.cellrule = self.cellrule
            c.pos = np.random.uniform(0, self.size-1,2) 
            c.brain_dna = reproduceable_cells[i].brain_dna 
        self.cells.extend(new_cells) 
    self.cells = [c for c in self.cells if c.alive]
    return 1

def env_rule3(self):
    pass

def env_rule4(self):
    pass
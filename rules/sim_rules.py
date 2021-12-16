import numpy as np

def default(self):
    if not np.any(self.cells):
        return 0
    
    self.call_all("live", self.clock, self.pos_map)
    self.clock += 1
    self.call_all("think")
    self.cells = [c for c in self.cells if c.alive]
    return 1

def rule2(self):
    pass

def rule3(self):
    pass

def rule4(self):
    pass
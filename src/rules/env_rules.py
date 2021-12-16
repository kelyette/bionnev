import numpy as np

def env_rule1(self):
    if not np.any(self.cells):
        return 0
    self.call_all(self.cellrule[0], self.clock, self.pos_map)
    self.clock += 1
    self.cells = [c for c in self.cells if c.alive]
    return 1

def env_rule2(self):
    pass

def env_rule3(self):
    pass

def env_rule4(self):
    pass
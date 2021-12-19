import numpy as np

class Cell:
    def __init__(self, envrule, cellrule):
        self.rule = cellrule
        self.alive = True
        self.age = 0
        self.reproduceable = False
        self.phys_dna = np.random.normal(0, 1, (len(self.rule.params["mean_physics"]))) * self.rule.params["std_physics"] + self.rule.params["mean_physics"]
        self.brain_dna = np.random.normal(0, 1, (self.rule.num_actions, self.rule.num_sensors))
        self.pos = np.rint(np.random.uniform(0, envrule.params["grid_size"] - 1, 2))
        self.sensors = np.zeros((self.rule.num_sensors, 1), dtype=float)
        self.actions = np.zeros((self.rule.num_actions, 1), dtype=float)
        self.set_attributes()
    
    def set_attributes(self, new_cell_rule=None):
        if new_cell_rule:
            self.rule = new_cell_rule
        for i, phys_attr in enumerate(self.rule.phys_attr):
            setattr(self, phys_attr, self.phys_dna[i]) 
        for other_attr in list(self.rule.other_attr.keys()):
            setattr(self, other_attr, self.rule.other_attr[other_attr])

    def live(self):
        self.age += 1
        if self.age >= self.death:
            self.die()

    def die(self):
        self.alive = False
    
    def think(self):
        if self.brain_dna.shape[1] != self.sensors.shape[0]:
            raise ValueError(f"The number of sensors ({self.sensors.shape[0]}) does not match the size of the defined sensors array ({self.brain_dna.shape[1]}). Check cell rule.")
        if self.brain_dna.shape[0] != self.actions.shape[0]:
            raise ValueError(f"The number of actions ({self.actions.shape[0]}) does not match the size of the defined actions array ({self.brain_dna.shape[0]}). Check cell rule.")
        self.actions = np.rint(1/(1+ np.exp(-1 * self.brain_dna @ self.sensors)))

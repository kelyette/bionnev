import numpy as np
class Cell:
    def __init__(self, envrule, cellrule):
        self.rule = cellrule
        self.grid_size = envrule.params["grid_size"]
        self.alive = True
        self.age = 0
        self.reproduceable = False
        self.phys_dna = np.random.normal(0, 1, (len(self.rule.params["mean_physics"]))) * self.rule.params["std_physics"] + self.rule.params["mean_physics"]
        self.brain_dna = np.random.normal(0, 1, (self.rule.num_actions, self.rule.num_sensors))
        self.death_age = self.phys_dna[0]
        self.pos = np.rint(np.random.uniform(0, self.grid_size - 1, 2))
        self.sensors = np.zeros((self.rule.num_actions, 1))
        self.actions = np.zeros((self.rule.num_sensors, 1))

    def live(self):
        self.age += 1
        if self.age >= self.death_age:
            self.die()

    def die(self):
        self.alive = False
    
    def think(self):
        self.actions = np.rint(1/(1+ np.exp(-1 * self.brain_dna @ self.sensors)))


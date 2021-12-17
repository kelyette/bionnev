import numpy as np

class Cell:
    def __init__(self, params):
        self.grid_size = params["grid_size"]
        self.alive = True
        self.age = 0
        self.reproduceable = False
        self.phys_dna = np.random.normal(0, 1, (len(params["mean_physics"]))) * params["std_physics"] + params["mean_physics"]
        self.brain_dna = np.random.normal(0, 1, (params["num_actions"], params["num_sensors"]))
        self.death_age = self.phys_dna[0]
        self.sex = int(self.phys_dna[1])
        self.strength = int(self.phys_dna[2])
        self.velocity = int(self.phys_dna[3])
        self.pos = np.rint(np.random.uniform(0, params["grid_size"]-1, 2))
        self.sensors = np.zeros((params["num_sensors"], 1))
        self.actions = np.zeros((params["num_actions"], 1))

    def live(self):
        self.age += 1
        if self.age >= self.death_age:
            self.die()

    def die(self):
        self.alive = False
    
    def think(self):
        self.actions = np.rint(1/(1+ np.exp(-1 * self.brain_dna @ self.sensors)))


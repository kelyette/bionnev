import numpy as np

class Cell:
    def __init__(self, params):
        self.grid_size = params["grid_size"]
        self.alive = True
        self.age = 0
        self.phys_dna = np.random.normal(0, 1, (len(params["mean_physics"]))) * params["std_physics"] + params["mean_physics"]
        self.brain_dna = np.random.normal(0, 0.01, (params["num_actions"], params["num_sensors"]))
        self.death_age = self.phys_dna[0]
        self.sex = self.phys_dna[1].round()
        self.strength = self.phys_dna[2]
        self.velocity = self.phys_dna[3].round()
        self.pos = np.random.uniform(0, params["grid_size"]-1, 2).round()
        self.sensors = np.zeros((params["num_sensors"], 1))
        self.actions = np.zeros((params["num_actions"], 1))

    def update_sensors(self, clock, pos_map):
        self.sensors = np.array([
            1,
            np.random.random(1).item(),
            np.sin(np.pi*clock/10).item(),
            self.pos[0] / self.grid_size,
            self.pos[1] / self.grid_size,
        ])
    def think(self):
        self.actions = (
            1 / (1 + np.exp(-1 * self.brain_dna @ self.sensors))).round()

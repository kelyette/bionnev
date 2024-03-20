import numpy as np

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from parameters.env_rules import EnvRule
    from parameters.cell_rules import CellRule

# cell class
# live and think get called every step
class Cell:
    def __init__(self, envrule: 'EnvRule', cellrule: 'CellRule', _id: int, *_, **env_attributes):
        self.id = _id
        self.rule = cellrule
        self.alive = True
        self.age = 0
        self.reproduceable = False
        for k, v in env_attributes.items():
            setattr(self, k, v)
        # create random dna from the rule's parameters
        self.phys_dna = np.random.normal(0, 1, (len(self.rule.params["mean_physics"]))) * self.rule.params["std_physics"] + self.rule.params["mean_physics"]
        self.brain_dna = np.random.normal(0, 1, (self.rule.num_actions, self.rule.num_sensors))
        # ... and initial position, velocity and acceleration
        self.pos = np.random.uniform(0, envrule.params["grid_size"], 2)
        self.pos = np.rint(np.random.uniform(0, envrule.params["grid_size"] - 1, 2))
        self.vel = np.zeros(2, dtype=float)
        self.acc = np.zeros(2, dtype=float)

        # sensors (input neurons)
        self.sensors = np.zeros((self.rule.num_sensors, 1), dtype=float)
        # actions (output neurons)
        self.actions = np.zeros((self.rule.num_actions, 1), dtype=float)
        self.set_attributes()

    def get_state(self):
        return {
            "id": self.id,
            "pos": self.pos.tolist(),
            "vel": self.vel.tolist(),
            "age": self.age, 
            "reproduceable": self.reproduceable,
        }
        
    # set all attributes from rule to the cell
    def set_attributes(self, new_cell_rule: 'CellRule' = None):
        if new_cell_rule:
            self.rule = new_cell_rule
        for i, phys_attr in enumerate(self.rule.phys_attr):
            setattr(self, phys_attr, self.phys_dna[i])
        for other_attr in list(self.rule.other_attr.keys()):
            setattr(self, other_attr, self.rule.other_attr[other_attr])

    # function to increment the age of the cell by 1 and check if
    # it's dead
    # gets called once every frame
    def live(self):
        self.age += 1
        if self.age >= self.death:
            self.die()

    # unalive the cell
    # completely pointless
    def die(self):
        self.alive = False
    
    # check if the dnas are of valid shape and if so, compute 
    # the neural network
    def step(self):
        if self.brain_dna.shape[1] != self.sensors.shape[0]:
            raise ValueError(f"The number of sensors ({self.sensors.shape[0]}) does not match the size of the defined sensors array ({self.brain_dna.shape[1]}). Check cell rule.")
        if self.brain_dna.shape[0] != self.actions.shape[0]:
            raise ValueError(f"The number of actions ({self.actions.shape[0]}) does not match the size of the defined actions array ({self.brain_dna.shape[0]}). Check cell rule.")

        self.actions = 1/(1+ np.exp(-1 * self.brain_dna @ self.sensors))

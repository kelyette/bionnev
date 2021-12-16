import numpy as np

def cell_rule1(self, clock, pos_map):
    move = (self.actions[:2].ravel() - self.actions[2:4].ravel()) * self.velocity
    self.pos += move - (move + self.pos > (self.grid_size-1)) * 2*((move + self.pos) - self.grid_size+1) - 2*(move + self.pos < 0) * ((move + self.pos))
    self.update_sensors(clock, pos_map)
    self.think()
    self.age += 1
    if self.age >= self.death_age:
        self.alive = False

#self.pos = np.maximum.reduce([np.minimum.reduce([self.pos + (self.actions[:2].ravel() - self.actions[2:4].ravel()) * self.velocity, np.ones(2)*(self.grid_size-1)]), np.zeros(2)])
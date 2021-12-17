import numpy as np

def cell_rule1(self, clock, pos_map):
    move = (self.actions[:2].ravel() - self.actions[2:4].ravel()) * self.velocity
    self.pos += move - (move + self.pos > (self.grid_size-1)) * 2*((move + self.pos) - self.grid_size+1) - (move + self.pos < 0) * 2*((move + self.pos))
    
    self.sensors = np.array([
        1,
    ])
    self.think()
    self.live() 

def cell_rule2(self, clock, pos_map):
    move = (self.actions[:2].ravel() - self.actions[2:4].ravel()) * self.velocity
    self.pos += move - (move + self.pos > (self.grid_size-1)) * 2*((move + self.pos) - self.grid_size+1) - (move + self.pos < 0) * 2*((move + self.pos))
    
    self.sensors = np.array([
        1,
        np.random.random(1).item(),
        np.random.uniform(1),
        int(self.pos[0] / self.grid_size),
        int(self.pos[1] / self.grid_size),
    ])
    self.think()
    self.live()    

#self.pos = np.maximum.reduce([np.minimum.reduce([self.pos + (self.actions[:2].ravel() - self.actions[2:4].ravel()) * self.velocity, np.ones(2)*(self.grid_size-1)]), np.zeros(2)])

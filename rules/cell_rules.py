def cell_rule1(self, clock, pos_map):
    self.move()
    self.update_sensors(clock, pos_map)
    self.think()
    self.age += 1
    if self.age >= self.death_age:
        self.alive = False
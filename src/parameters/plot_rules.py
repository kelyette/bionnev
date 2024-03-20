from classes.plotting import Plot

class Rule1(Plot):
    def __init__(self):
        self.display_name = 'Default'
        self.exp = 'Default'
        self.show_n = 1
        self.fps = 250
        self.rules = [
            {'show_cond': True, 'cell_cond': lambda cell: not cell.reproduceable, 'color_num': 2},
            {'show_cond': lambda env: env.clock > 5, 'cell_cond': lambda cell: cell.age <= 5, 'color_num': 1},
            {'show_cond': True, 'cell_cond': lambda cell: cell.reproduceable, 'color_num': 4},
            {'show_cond': True, 'cell_cond': lambda cell: 3 < cell.id < 10, 'color_num': 3},
        ]
        self.stats = {
            'Simulation day': lambda sim: sim.env.clock,
            'Number of cells': lambda sim: len(sim.env.cells),
            'Mean age' : lambda sim: sum([cell.age/len(sim.env.cells) for cell in sim.env.cells]),
            'FPS': lambda sim: 1 / sim.update_took if sim.update_took != 0 else 0,
            'avg cell accx': lambda sim: sum(cell.acc[0] for cell in sim.env.cells)/len(sim.env.cells),
            'avg cell accy': lambda sim: sum(cell.acc[1] for cell in sim.env.cells)/len(sim.env.cells),
        }
        super().__init__()
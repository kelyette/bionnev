from classes.plotting import Plot
import numpy as np

class Rule1(Plot):
    def __init__(self):
        self.display_name = 'oui'
        self.exp = 'hihi'
        self.colors = np.array([
            [255, 255, 255], # WHITE
            [164, 55, 72],   # RED
            [174, 117, 58],  # YELLOW
            [39, 93, 108],   # BLUE
            [76, 148, 50],   # GREEN
        ])
        self.show_n = 1
        self.fps = 100
        self.rules = [
            {'show_cond': True, 'cell_cond': lambda cell: not cell.reproduceable, 'color_num': 2},
            {'show_cond': True, 'cell_cond': lambda cell: cell.reproduceable, 'color_num': 4},
            {'show_cond': lambda env: env.clock > 5, 'cell_cond': lambda cell: cell.age <= 5, 'color_num': 1},
        ]
        self.stats = {
            'Simulation day': lambda sim: sim.env.clock,
            'Number of cells': lambda sim: len(sim.env.cells),
            'Mean age' : lambda sim: sum([cell.age/len(sim.env.cells) for cell in sim.env.cells]),
            'FPS': lambda sim: 1 / sim.update_took if sim.update_took != 0 else 0
        }
        super().__init__()

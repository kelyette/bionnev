from src.plotting import Plot
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
            'Simulation day': lambda env: env.clock,
            'Number of cells': lambda env: len(env.cells),
            'Mean age' : lambda env: sum([cell.age/len(env.cells) for cell in env.cells])
        }
        super().__init__()

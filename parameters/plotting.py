import numpy as np

class Plot:
    def __init__(self):
        self.colors = np.array([
            [255, 255, 255], # WHITE
            [164, 55, 72],   # RED
            [174, 117, 58],  # YELLOW
            [39, 93, 108],   # BLUE
            [76, 148, 50],   # GREEN
        ])
        self.show_n = 100
        self.fps = 100




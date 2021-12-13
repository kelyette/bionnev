import numpy as np
import math
import yaml

with open("params.yaml", "r") as f:
    params = yaml.safe_load(f)["one"]

print(params)

class Cell:
    def __init__(self):
        pos = np.random.uniform(0, params["grid-size"], 2)
        
        # gene = self.create_gene()
        
        while True:
            print(self.create_gene(), end="\r")
        
        self.cellinfo = "".join(str(i) for i in (pos, gene))
    
    def create_gene(self):
        neuron_length = params["init-neurons"]
        fac_nl = math.factorial(neuron_length)
        gene = np.random.randint((fac_nl*2)-1)
        
        return gene
    
    def brain(self):
        neuron_input = self.cellinfo

        final_action = np.logical_xor(neuron_input, self.gene)
        
        self.cellinfo = final_action
        
        
c1 = Cell()
import torch
from torch import nn
import numpy as np

class FeedForwardNN(nn.Module):
    def __init__(self, input_size, output_size, hidden_shape):
        super(FeedForwardNN, self).__init__()

        layers = []
        for i, hidden_size in enumerate(hidden_shape):
            layers.append(nn.Linear(input_size if i == 0 else hidden_shape[i-1], hidden_size))
            layers.append(nn.ReLU())
        
        layers.append(nn.Linear(hidden_shape[-1], output_size))
        self.layers = nn.Sequential(*layers)

    def forward(self, inputs, weights=None, bias=0):
        inputs = torch.tensor(inputs, dtype=torch.float32)
        nninputs = inputs if weights is None else inputs @ weights
        nninputs += bias
        return self.layers(nninputs).detach().numpy()


class LinearNN():
    @staticmethod
    def compute(inputs, weights, bias=0):
        return 1/(1+ np.exp(-1 * inputs @ weights + bias))
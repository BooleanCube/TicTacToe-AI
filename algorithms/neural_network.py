import numpy as np

_INPUT_LAYER = 0
_HIDDEN_LAYER = 1
_OUTPUT_LAYER = 2
_learn_rate = 5e-5


class Neuron:
    def __init__(self, next_layer_size):
        self.w = [np.random.uniform(-0.5, 0.5) for _ in range(next_layer_size)]
        self.b = self.a = 0


class Layer:
    def __init__(self, type, size, next_layer_size=0):
        self.type = type
        self.neurons = [Neuron(next_layer_size) for _ in range(size)]


class NeuralNetwork:
    def __init__(self):
        self.layers = [
            Layer(_INPUT_LAYER, 25, 50),
            Layer(_HIDDEN_LAYER, 50, 50),
            Layer(_HIDDEN_LAYER, 50, 25),
            Layer(_OUTPUT_LAYER, 25)
        ]

    @staticmethod
    def _relu(val):
        return max(0, val)

    @staticmethod
    def _sigmoid(val):
        return 1 / (1 + np.exp(-val))

    def feed_forward(self, board):
        for v in range(len(board)):
            self.layers[0].neurons[v].a = board[v]
        for l in range(len(self.layers) - 1):
            cur_layer = self.layers[l]
            next_layer = self.layers[l+1]
            for i in range(len(cur_layer.neurons)):
                for j in range(len(cur_layer.neurons[i].w)):
                    next_layer.neurons[j].a += cur_layer.neurons[i].w[j] * cur_layer.neurons[i].a + cur_layer.neurons[i].b
            for neuron in next_layer.neurons:
                if next_layer.type == _OUTPUT_LAYER:
                    neuron.a = self._sigmoid(neuron.a)
                else:
                    neuron.a = self._relu(neuron.a)


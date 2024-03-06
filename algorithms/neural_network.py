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
    def __init__(self, dim):
        size = dim ** 2
        self.layers = [
            Layer(_INPUT_LAYER, size, 20),
            Layer(_HIDDEN_LAYER, 20, size),
            # Layer(_HIDDEN_LAYER, 15, size),
            Layer(_OUTPUT_LAYER, size)
        ]

    @staticmethod
    def _relu(val):
        return max(0, val)

    @staticmethod
    def _sigmoid(val):
        return 1 / (1 + np.exp(-val))

    def temp_feed_forward(self, board):
        input_layer = self.layers[0]
        hidden_layer = self.layers[1]
        output_layer = self.layers[2]
        for v in range(len(board)):
            input_layer.neurons[v].a = (0 if board[v] == 0 else 0.5 if board[v] == 2 else 1)
        for j in range(len(hidden_layer.neurons)):
            for i in range(len(input_layer.neurons)):
                hidden_layer.neurons[j].a += input_layer.neurons[i].w[j] * input_layer.neurons[i].a
            hidden_layer.neurons[j].a += hidden_layer.neurons[j].b
            hidden_layer.neurons[j].a = self._sigmoid(hidden_layer.neurons[j].a)
        for j in range(len(output_layer.neurons)):
            for i in range(len(hidden_layer.neurons)):
                output_layer.neurons[j].a += hidden_layer.neurons[i].w[j] * hidden_layer.neurons[i].a
            output_layer.neurons[j].a += output_layer.neurons[j].b
            output_layer.neurons[j].a = self._sigmoid(output_layer.neurons[j].a)
        return list(map(lambda x: x.a, output_layer.neurons))

    def feed_forward(self, board):
        for v in range(len(board)):
            self.layers[0].neurons[v].a = (0 if board[v] == 0 else 0.5 if board[v] == 2 else 1)
        for l in range(len(self.layers) - 1):
            cur_layer = self.layers[l]
            next_layer = self.layers[l+1]
            for j in range(len(next_layer.neurons)):
                for i in range(len(cur_layer.neurons)):
                    next_layer.neurons[j].a += cur_layer.neurons[i].w[j] * cur_layer.neurons[i].a
                next_layer.neurons[j].a += next_layer.neurons[j].b
                next_layer.neurons[j].a = self._sigmoid(next_layer.neurons[j].a)
        return list(map(lambda x: x.a, self.layers[-1].neurons))

    def temp_back_propagate(self, label):
        input_layer = self.layers[0]
        hidden_layer = self.layers[1]
        output_layer = self.layers[2]

        # update the delta values
        for i in range(len(output_layer.neurons)):
            v = output_layer.neurons[i].a
            output_layer.neurons[i].a -= (1 if label == i else 0)



    def back_propagate(self, label):
        # update the delta values
        for i in range(len(self.layers[-1].neurons)):
            v = self.layers[-1].neurons[i].a
            self.layers[-1].neurons[i].a = (1 if label == i else 0) - v

        # propagate on the neural network
        for l in range(len(self.layers)-1, 0, -1):
            cur_layer = self.layers[l]
            prev_layer = self.layers[l-1]

            # update weights
            for i in range(len(prev_layer.neurons)):
                for j in range(len(prev_layer.neurons[i].w)):
                    prev_layer.neurons[i].w[j] += _learn_rate * cur_layer.neurons[j].a
            # update biases
            for neuron in cur_layer.neurons:
                neuron.b += _learn_rate * neuron.a

            # update layer's neuron activation values to propagate backwards
            for i in range(len(prev_layer.neurons)):
                cur_neuron = prev_layer.neurons[i]
                derivative = cur_neuron.a * (1 - cur_neuron.a)
                sum_gradient = 0
                for j in range(len(cur_neuron.w)):
                    sum_gradient += cur_neuron.w[j] * cur_layer.neurons[j].a
                cur_neuron.a = derivative * sum_gradient

        self.clear_activations()

    def clear_activations(self):
        for layer in self.layers:
            for neuron in layer.neurons:
                neuron.a = 0

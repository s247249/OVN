# 1. Define the class Signal information that has the following attributes:
#    • signal power: float
#    • noise power: float
#    • latency: float
#    • path: list[string]
#    such that its constructor initializes the signal power to a given value, the
#    noise power and the latency to zero and the path as a given list of letters
#    that represents the labels of the nodes the signal has to travel through. The
#    attribute latency is the total time delay due to the signal propagation
#    through any network element along the path. Define the methods to
#    update the signal and noise powers and the latency given an increment
#    of these quantities. Define a method to update the path once a node is
#    crossed.
class SignalInformation:
    def __init__(self, signal_power, path, noise_power=0, latency=0):
        self._signal_power = float(signal_power)
        self._noise_power = float(noise_power)
        self._latency = float(latency)
        self._path = list(path)

    @property
    def signal_power(self):
        return self._signal_power

    @property
    def noise_power(self):
        return self._noise_power

    @property
    def latency(self):
        return self._latency

    @property
    def path(self):
        return self._path

    @signal_power.setter
    def signal_power(self, signal_power):
        self._signal_power = signal_power

    @noise_power.setter
    def noise_power(self, noise_power):
        self._noise_power = noise_power

    @latency.setter
    def latency(self, latency):
        self._latency = latency

    @path.setter
    def path(self, path):
        self._path = path

    def update_signal_power(self, signal_power):
        sp = self._signal_power + signal_power
        self.signal_power = sp

    def update_noise_power(self, noise_power):
        np = self._noise_power + noise_power
        self.noise_power = np

    def update_latency(self, latency):
        l = self._latency + latency
        self.latency = l

    def update_path(self, new_node):
        self.path.append(new_node)


# 2. Define the class Node that has the following attributes:
#    • label: string
#    • position: tuple(float, float)
#    • connected nodes: list[string]
#    • successive: dict[Line]
#    such that its constructor initializes these values from a python dictionary
#    input. The attribute successive has to be initialized to an empty dictio-
#    nary. Define a propagate method that update a signal information object
#    modifying its path attribute and call the successive element propagate
#    method, accordingly to the specified path.
class Node:
    def __init__(self, py_dict):
        self._label = str(py_dict['label'].values)
        self._position = tuple(py_dict['position'].values)
        self._connected_nodes = list(str(py_dict('connected_nodes')))
        self._successive = dict()

    @property
    def label(self):
        return self._label

    @property
    def position(self):
        return self._position

    @property
    def connected_nodes(self):
        return self._connected_nodes

    @property
    def successive(self):
        return self._successive

    @label.setter
    def label(self, label):
        self._label = label

    @position.setter
    def position(self, position):
        self._position = position

    @connected_nodes.setter
    def connected_nodes(self, nodes):
        self._connected_nodes = nodes

    @successive.setter
    def successive(self, nodes_dict):
        self._successive = nodes_dict

    def propagate(self, signal):
        signal.update_path(self.label)
        self.successive[self.label].propagate(signal)


# 3. Define the class Line that has the following attributes:
#    • label: string
#    • length: float
#    • successive: dict[Node]
#    The attribute successive has to be initialized to an empty dict. Define the
#    following methods that update an instance of the signal information:
#    • latency generation(): float
#    • noise generation(signal power): 1e-9 * signal power * length
#    The light travels through the fiber at around 2/3 of the speed of light
#    in the vacuum. Define the line method latency generation accordingly.
#    Define a propagate method that updates the signal information modifying
#    its noise power and its latency and call the successive element propagate
#    method, accordingly to the specified path.
class Line:
    def __init__(self, label, length):
        self._label = label
        self._length = length
        self._successive = dict()

    @property
    def label(self):
        return self._label

    @property
    def length(self):
        return self._length

    @property
    def successive(self):
        return self._successive

    @label.setter
    def label(self, label):
        self._label = label

    @length.setter
    def length(self, length):
        self._length = length

    @successive.setter
    def successive(self, successive):
        self._successive = successive

    def latency_generation(self, signal):
        l = float(self._length / (3e8 * 2/3))
        signal.update_latency(l)

    def noise_generation(self, signal):
        n = 1e-9 * signal.signal_power * signal.length
        signal.update_noise_power(n)

    def propagate(self, signal):
        self.latency_generation(signal)
        self.noise_generation(signal)
        self._successive.propagate(signal)


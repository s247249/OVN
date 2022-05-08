class Line:
    def __init__(self, label, length, number_of_channels):
        self._label = label
        self._length = length
        self._successive = dict()
        self._state = list()

        for i in range(number_of_channels):
            self._state.append(1)

    @property
    def label(self):
        return self._label

    @property
    def length(self):
        return self._length

    @property
    def successive(self):
        return self._successive

    @property
    def state(self):
        return self._state

    @label.setter
    def label(self, label):
        self._label = label

    @length.setter
    def length(self, length):
        self._length = length

    def set_state(self, index, state):
        self._state[index] = state

    def set_successive(self, node):
        self._successive[node.label] = node

    def latency_generation(self):
        return float(self._length / (3e8 * 2/3))

    def noise_generation(self, signal_power):
        return float(1e-9 * signal_power * self.length)

    def propagate(self, signal):
        latency = self.latency_generation()
        noise = self.noise_generation(signal.signal_power)
        signal.update_latency(latency)
        signal.update_noise_power(noise)
        for i in self.successive.values():
            i.propagate(signal)

    def probe(self, signal):
        latency = self.latency_generation()
        noise = self.noise_generation(signal.signal_power)
        signal.update_latency(latency)
        signal.update_noise_power(noise)
        for i in self.successive.values():
            i.probe(signal)

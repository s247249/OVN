from ..added_methods.lab05_line import Line5 as line5
from ..added_methods.lab06_line import Line6 as line6
from ..extras.NLI_var import NliVar


class Line:
    def __init__(self, label, length, number_of_channels):
        self._label = label
        self._length = length
        self._successive = dict()
        self._state = list()

        self._n_amplifiers = 2
        # dB
        self._gain = 16
        # dB
        self._noise_figure = 3
        self._NLI_var = NliVar

        for i in range(number_of_channels):
            self._state.append(1)

        len = int(self._length)
        while len > 0:
            len -= 80e3
            if len > 0:
                self._n_amplifiers += 1

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

    @property
    def n_amplifiers(self):
        return self._n_amplifiers

    @property
    def gain(self):
        return self._gain

    @property
    def noise_figure(self):
        return self._noise_figure

    @property
    def NLI_var(self):
        return self._NLI_var

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

    # 1. Modify the method noise generation within the class Line including
    #    the methods for the computation of the ASE and the NLI and removing
    #    the old formula.
    def noise_generation(self, signal_power):
        ASE = line5.ase_generation(self)
        NLI = line5.nli_generation(self, signal_power)
        noise_list = (ASE, NLI)
        return noise_list

    def propagate(self, signal):
        latency = self.latency_generation()

        sig_pow = self.optimized_launch_power(signal.signal_power)

        noise = self.noise_generation(sig_pow)
        signal.update_latency(latency)
        signal.update_noise_power(noise[0] + noise[1])
        for i in self.successive.values():
            i.propagate(signal)

    def probe(self, signal):
        latency = self.latency_generation()
        noise = self.noise_generation(signal.signal_power)
        signal.update_latency(latency)
        signal.update_noise_power(noise)
        for i in self.successive.values():
            i.probe(signal)

    def ase_generation(self):
        return line5.ase_generation(self)

    def nli_generation(self, P_ch):
        return line5.nli_generation(self, P_ch)

    def optimized_launch_power(self, signal_power):
        return line6.optimized_launch_power(self, signal_power)
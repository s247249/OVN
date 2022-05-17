from ..added_methods.lab05_line import Line5 as line5
from ..extras.NLI_var import NliVar


class Line:
    def __init__(self, label, length, number_of_channels):
        self._label = label
        self._length = length
        self._successive = dict()
        self._state = list()

        # 1. Include in the class Line the attribute n_amplifiers that express the
        #    number of optical amplifiers on that line. This number has to be cal-
        #    culated using the line length, supposing that an amplifier is necessary
        #    every 80 km. A line includes an additional amplifier at each terminal
        #    (the BOOSTER and the Pre-Amplifier). Moreover, include the attributes
        #    gain and noise_figure that are fixed for each amplifier to 16 dB and 3 dB,
        #    respectively.
        self._n_amplifiers = 2
        # dB
        self._gain = 16
        # dB
        self._noise_figure = 3

        # 3. Include in the class Line an attribute for the following physical features of
        #    the fibers necessary to evaluate the nonlinear interference noise, supposing
        #    that all the lines are composed of the same fiber variety:
        #    Remember that alpha = alpha_dB/(10log10(e)) and L_eff = 1/alpha
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

    def ase_generation(self):
        return line5.ase_generation(self)

    def nli_generation(self, P_ch):
        return line5.nli_generation(self, P_ch)

from .added_methods.lab05_line import Line5
from .added_methods.lab06_line import Line6
from .extras.NLI_var import NliVar


class Line(Line5, Line6):
    def __init__(self, label, length, number_of_channels):
        self._label = label
        self._length = length
        self._successive = dict()
        self._state = list()
        self._number_of_channels = number_of_channels
        self._n_amplifiers = 2
        # dB
        self._gain = 16
        # dB
        # self._noise_figure = 3
        self._noise_figure = 5
        self._NLI_var = NliVar()

        # 3. Add to the class Line an attribute called in service which is a Boolean
        #    and it is initialized to 1 (1 {> IN SERVICE, 0 {> OUT OF SERVICE).
        self._in_service = bool(1)

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

    @property
    def number_of_channels(self):
        return self._number_of_channels

    @property
    def in_service(self):
        return self._in_service

    @label.setter
    def label(self, label):
        self._label = label

    @length.setter
    def length(self, length):
        self._length = length

    @length.setter
    def in_service(self, in_service):
        self._in_service = in_service

    def set_state(self, index, state):
        self._state[index] = state

    def set_successive(self, node):
        self._successive[node.label] = node

    def latency_generation(self):
        return float(self._length / (3e8 * 2/3))

    def noise_generation(self, signal_power):
        ASE = self.ase_generation()
        NLI = self.nli_generation(signal_power)
        noise_list = (ASE, NLI)
        return noise_list

    def propagate(self, signal):
        latency = self.latency_generation()

        sig_pow = self.optimized_launch_power()
        if sig_pow > signal.signal_power:
            signal.signal_power = sig_pow

        # noise[0] = ASE
        # noise[1] = NLI
        noise = self.noise_generation(sig_pow)
        signal.GSNR.append(sig_pow/(noise[0] + noise[1]))

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

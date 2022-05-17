class SignalInformation:
    def __init__(self, signal_power):
        self._signal_power = float(signal_power)
        self._noise_power = float(0)
        self._latency = float(0)
        self._path = list()

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
        self.signal_power += sp

    def update_noise_power(self, noise_power):
        np = self._noise_power + noise_power
        self.noise_power += np

    def update_latency(self, latency):
        self.latency += latency

    def update_path(self):
        del self.path[0]
        if len(self.path) > 0:
            return self.path[0]
        else:
            return 0


# 4. Include in the class Lightpath the attributes Rs and df which represent
#    the signal symbol rate and the frequency spacing between two consecutive
#    channels.
class Lightpath(SignalInformation):
    def __init__(self, signal_power, channel, Rs, df):
        super().__init__(signal_power)
        self._channel = channel
        self._Rs = Rs
        self._df = df

    @property
    def channel(self):
        return self._channel

class Connection:
    def __init__(self, input, output, signal_power):
        self._input = str(input)
        self._output = str(output)
        self._signal_power = float(signal_power)
        self._latency = float(0)
        self._snr = float(0)
        self._bit_rate = float(0)

    @property
    def input(self):
        return self._input

    @property
    def output(self):
        return self._output

    @property
    def signal_power(self):
        return self._signal_power

    @property
    def latency(self):
        return self._latency

    @property
    def snr(self):
        return self._snr

    @property
    def bit_rate(self):
        return self._bit_rate

    @latency.setter
    def latency(self, latency):
        self._latency = latency

    @snr.setter
    def snr(self, snr):
        self._snr = snr

    @bit_rate.setter
    def bit_rate(self, Rb):
        self._bit_rate = Rb
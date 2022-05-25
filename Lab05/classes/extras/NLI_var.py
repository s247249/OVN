class NliVar:
    def __init__(self):
        # dB/m
        self._alpha_dB = 0.2e-3
        # (m*Hz^2)-1
        self._beta_2 = 2.13e-26
        # (m*W)^-1
        self._gamma = 1.27e-3
        # GHz
        self._Rs = 32
        # GHz
        self._df = 50
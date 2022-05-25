class NliVar:
    def __init__(self):
        # dB/m
        self.alpha_dB = 0.2e-3
        # (m*Hz^2)-1 = (s^2/m)
        self.beta_2 = 2.13e-26
        # (m*W)^-1
        self.gamma = 1.27e-3
        # Hz
        self.Rs = 32e9
        # Hz
        self.df = 50e9

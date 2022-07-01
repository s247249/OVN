import math


# 2. Define in the class Line the method ase_generation that evaluate the to-
#    tal amount of amplified spontaneous emissions (ASE) in linear units gen-
#    erated by the amplifiers supposing that a cascade of amplifiers introduces
#    a noise amount which follows the expression:
#        ASE = N (h f Bn NF [G - 1])
#    where N is the number of amplifiers, h is the Plank constant, f is the
#    frequency which would be fixed to 193.414 THz (C-band center), Bn is
#    the noise bandwidth fixed to 12.5 GHz, NF and G are the amplifier noise
#    figure and gain, respectively.
class Line5:
    def ase_generation(self):
        N = self.n_amplifiers
        # from slides: J*s
        h = 6.66e-34
        # Hz
        f = 193.414e12
        # Hz
        Bn = 12.5e9
        # from dB to pure
        NF = 10 ** (self.noise_figure / 10)
        # from dB to pure
        G = 10 ** (self.gain / 10)
        ASE = N * (h * f * Bn * NF * (G - 1))
        return ASE

    # 5. Define in the class Line the method nli_generation that evaluates the
    # total amount generated by the nonlinear interface noise using the formula
    # (in linear units):
    # NLI = P_ch^3 eta_nli N_span Bn
    # where Bn is the noise bandwidth (12.5 GHz) and Nspan is the number of
    # fiber span within the considered line.
    def nli_generation(self, P_ch):
        # Hz
        Bn = 12.5e9
        N_span = (self.n_amplifiers - 1)
        # 1/m
        alpha = self.NLI_var.alpha_dB / (10 * math.log(math.e, 10))
        log = math.log((math.pi ** 2)
                       * self.NLI_var.beta_2 * (self.NLI_var.Rs ** 2)
                       * (self.number_of_channels ** (2 * self.NLI_var.Rs / self.NLI_var.df))
                       / (2 * alpha), math.e)
        eta_nli = 16 / (27 * math.pi) * log \
                  * (self.NLI_var.gamma ** 2) / (4 * alpha * self.NLI_var.beta_2 * (self.NLI_var.Rs ** 3))

        NLI = (P_ch ** 3) * eta_nli * N_span * Bn

        return NLI

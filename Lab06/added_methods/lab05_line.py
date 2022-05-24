import math

class Line5:
    def ase_generation(self):
        N = self.n_amplifiers
        h = 6.6260693e-34
        # THz
        f = 193.414
        # THz
        Bn = 12.5e-3
        NF = self.noise_figure
        G = self.gain

        ASE = N * (h * f * Bn * NF * [G - 1])
        return ASE

    def nli_generation(self, P_ch):
        # THz
        Bn = 12.5e-3
        N_span = (self.n_amplifiers - 1)
        alpha = self.NLI_var.alpha_dB / (10 * math.log(math.e, 10))
        log = math.log((math.pi ** 2)
                       * self.NLI_var.beta_2 * (self.NLI_var.Rs ** 2)
                       * (self.number_of_channels ** (2 * self.NLI_var.Rs/N_span))
                       / (2 * alpha), math.e)
        eta_nli = 16/(27 * math.pi) * log \
                  * (self.NLI_var.gamma ^ 2) / (4 * alpha * self.NLI_var.beta_2 * (self.NLI_var.Rs ** 3))

        NLI = (P_ch ** 3) * eta_nli * N_span * Bn

        return NLI

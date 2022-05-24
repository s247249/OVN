import math
# 2. Create a new method optimized launch power in the class Line for
#    the determination of the optimal launch power.
#    Hint: start from the definition of the GSNR and introduce the expressions
#    of ASE and NLI power adopted in your code.
class Line6:
    def optimized_launch_power(self, signal_power):
        # GSNR = Pch/(ASE + NLI)
        # P_opt = sqrt3 (Fi * Li * Pbase / (2 * Bch * etaNLI * spans)
        # Pbase = h*f0*Bch
        h = 6.6260693e-34
        f0 = 193414
        Bch = 12.5

        N_span = (self.n_amplifiers - 1)
        alpha = self.NLI_var.alpha_dB / (10 * math.log(math.e, 10))
        L = 1/alpha
        NF = self.noise_figure
        log = math.log((math.pi ** 2)
                       * self.NLI_var.beta_2 * (self.NLI_var.Rs ** 2)
                       * (self.number_of_channels ** (2 * self.NLI_var.Rs / N_span))
                       / (2 * alpha), math.e)
        eta_nli = 16 / (27 * math.pi) * log \
                  * (self.NLI_var.gamma ^ 2) / (4 * alpha * self.NLI_var.beta_2 * (self.NLI_var.Rs ** 3))

        P_opt = (NF * L * h * f0 * Bch / (2 * Bch * eta_nli * N_span)) ** (1/3)

        return P_opt

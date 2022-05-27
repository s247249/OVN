# 8. Run again the main script modifying the value of beta_2 to 0.6 e-26 (m Hz2)^-1.
#    Compare the result by means of the average GSNR and the total allocated
#    capacity.

# RES with T:           300 - 600 - 1500
# old:  avg GSNR:       90  - 80  - 86 dB
#       capacity:       9   - 18  - 49 Tb/s
# new:  avg GSNR:       67  - 60  - 67 dB
#       capacity:       9   - 18  - 56 Tb/s
class NliVar:
    def __init__(self):
        # dB/m
        self.alpha_dB = 0.2e-3

        # (m*Hz^2)-1 = (s^2/m)
        self.beta_2 = 2.13e-26
        # self.beta_2 = 0.6e-26

        # (m*W)^-1
        self.gamma = 1.27e-3
        # Hz
        self.Rs = 32e9
        # Hz
        self.df = 50e9

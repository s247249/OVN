import math
from scipy.special import erfinv


# 1. Implement a method calculate bit rate(path, strategy) in the Net-
#    work class that evaluates the bit rate Rb supported by a specific path
#    given the corresponding GSNR (in linear units) and the transceiver tech-
#    nology using the following equations:

#    where (1) is for the fixed-rate transceiver strategy assuming PM-QPSK
#    modulation, (2) is for the flex-rate transceiver strategy assuming the
#    availability of PM-QPSK (100Gbps), PM-8-QAM (200Gbps) and PM-
#    16QAM (400Gbps) modulations, given a BERt of 10^-3. In conclusion, (3)
#    is the maximum theoretical Shannon rate with an ideal Gaussian modula-
#    tion. Rs is the symbol-rate of the light-path that can be fixed to 32 GHz
#    and Bn is the noise bandwidth (12.5 GHz).
class Network4:
    def calculate_bit_rate(self, path, strategy):
        BER_t = 1e-3
        Rs = 32
        Bn = 12.5

        cnt = 0
        for i in self.weighted_paths['Path']:
            if path == i:
                break
            cnt += 1

        GSNR_dB = (self.weighted_paths['SNR (dB)'][cnt])
        GSNR = 10 ** (GSNR_dB/10)

        if strategy == 'fixed-rate':
            if GSNR >= 2 * ((erfinv(2 * BER_t)) ** 2) * Rs/Bn:
                Rb = 100
            else:
                Rb = 0

        elif strategy == 'flex-rate':
            if GSNR < 2 * ((erfinv(2 * BER_t)) ** 2) * Rs/Bn:
                Rb = 0
            elif GSNR < 14/3 * ((erfinv(3/2 * BER_t)) ** 2) * Rs/Bn:
                Rb = 100
            elif GSNR < 10 * ((erfinv(8/3 * BER_t)) ** 2) * Rs/Bn:
                Rb = 200
            else:
                Rb = 400

        elif strategy == 'shannon-rate':
            Rb = 2 * Rs * math.log(1+GSNR+Rs/Bn, 2)

        return Rb

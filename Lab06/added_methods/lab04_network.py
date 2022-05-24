import matplotlib.pyplot as plt
import math
from scipy.special import erfcinv


class Network4:
    def calculate_bit_rate(self, path, strategy):
        BER_t = 1e-3
        Rs = 32
        Bn = 12.5
        Rb = -1

        cnt = 0
        for i in self.weighted_paths['Path']:
            if path == i:
                break
            cnt += 1

        GSNR_dB = (self.weighted_paths['SNR (dB)'][cnt])
        GSNR = 10 ** (GSNR_dB/10)

        if strategy == 'fixed-rate':
            if GSNR >= 2 * ((erfcinv(2 * BER_t)) ** 2) * Rs/Bn:
                Rb = 100
            else:
                Rb = 0

        elif strategy == 'flex-rate':
            if GSNR < 2 * ((erfcinv(2 * BER_t)) ** 2) * Rs/Bn:
                Rb = 0
            elif GSNR < 14/3 * ((erfcinv(3/2 * BER_t)) ** 2) * Rs/Bn:
                Rb = 100
            elif GSNR < 10 * ((erfcinv(8/3 * BER_t)) ** 2) * Rs/Bn:
                Rb = 200
            else:
                Rb = 400

        elif strategy == 'shannon':
            Rb = 2 * Rs * math.log(1+GSNR+Rs/Bn, 2)

        else:
            print('Wrong strategy')

        return Rb

    def graph(self):

        BER_t = 1e-3
        Rs = 32
        Bn = 12.5

        plt.figure()

        # 0 Bit Rate
        x2 = 2 * ((erfcinv(2 * BER_t)) ** 2) * Rs / Bn
        x = (0, 10 * math.log(x2, 10))
        y = (0, 0)
        plt.plot(x, y, color='r', linestyle='-')

        # up
        x = (10 * math.log(x2, 10), 10 * math.log(x2, 10))
        y = (0, 100)
        plt.plot(x, y, color='r', linestyle='-')

        # PM-QPSK (100Gbps)
        x1 = float(x2)
        x2 = 14 / 3 * ((erfcinv(3 / 2 * BER_t)) ** 2) * Rs / Bn
        x = (10 * math.log(x1, 10), 10 * math.log(x2, 10))
        y = (100, 100)
        plt.plot(x, y, color='r', linestyle='-')

        # up
        x = (10 * math.log(x2, 10), 10 * math.log(x2, 10))
        y = (100, 200)
        plt.plot(x, y, color='r', linestyle='-')

        # PM-8-QAM (200Gbps)
        x1 = float(x2)
        x2 = 10 * ((erfcinv(8 / 3 * BER_t)) ** 2) * Rs / Bn
        x = (10 * math.log(x1, 10), 10 * math.log(x2, 10))
        y = (200, 200)
        plt.plot(x, y, color='r', linestyle='-')

        # up
        x = (10 * math.log(x2, 10), 10 * math.log(x2, 10))
        y = (200, 400)
        plt.plot(x, y, color='r', linestyle='-')

        # PM-16QAM (400Gbps)
        x1 = float(x2)
        # max GSNR arbitrarily put at 100 (linear)
        x2 = 2 * Rs * math.log(1 + 100 + Rs / Bn, 2)
        x = (10 * math.log(x1, 10), 10 * math.log(x2, 10))
        y = (400, 400)
        plt.plot(x, y, color='r', linestyle='-')

        plt.xlabel('GSNR (dB)')
        plt.ylabel('Bit Rate (Gbps)')

        plt.show()

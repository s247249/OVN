import matplotlib.pyplot as plt
import math
from scipy.special import erfcinv


class Network4:
    def calculate_bit_rate(self, l_path, strategy):
        BER_t = 1e-3
        # GHz
        Rs = l_path.Rs
        # GHz
        Bn = 12.5
        Rb = 0

        sigma = 0
        for i in range(len(l_path.GSNR)):
            sigma += 1/l_path.GSNR[i]
        GSNR = 1/sigma

        l_path.GSNR_tot = GSNR

        """GSNR1 = l_path.signal_power/l_path.noise_power
        print('\n' + str(GSNR) + '\t\t' + str(GSNR1))"""
        # GSNR_dB = 10 * math.log(GSNR, 10)

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
            Rb = 2 * Rs * math.log(1+GSNR*Rs/Bn, 2)

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
        plt.plot(x, y, color='darkorchid', linestyle='-')

        # up
        x = (10 * math.log(x2, 10), 10 * math.log(x2, 10))
        y = (0, 100)
        plt.plot(x, y, color='darkorchid', linestyle='-')

        # PM-QPSK (100Gbps)
        x1 = float(x2)
        x2 = 14 / 3 * ((erfcinv(3 / 2 * BER_t)) ** 2) * Rs / Bn
        x = (10 * math.log(x1, 10), 10 * math.log(x2, 10))
        y = (100, 100)
        plt.plot(x, y, color='darkorchid', linestyle='-')

        x1 = 14 / 3 * ((erfcinv(3 / 2 * BER_t)) ** 2) * Rs / Bn
        x = (10 * math.log(x1, 10), 30)
        y = (100, 100)
        plt.plot(x, y, color='royalblue', linestyle='-')

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
        """x2 = 2 * Rs * math.log(1 + 100 + Rs / Bn, 2)
        x = (10 * math.log(x1, 10), 10 * math.log(x2, 10))"""
        x = (10 * math.log(x1, 10), 30)
        y = (400, 400)
        plt.plot(x, y, color='r', linestyle='-')

        x_dB = np.linspace(0, 30, 100)
        x = 10 ** (x_dB / 10)
        # Rb = 2 * Rs * math.log(1 + GSNR * Rs / Bn, 2)
        y = 2 * Rs * np.log2(1 + (x * Rs / Bn))
        plt.plot(x_dB, y, color='limegreen', linestyle='-')

        plt.xlabel('GSNR (dB)')
        plt.ylabel('Bit Rate (Gbps)')

        plt.annotate(f'Fixed-Rate',
                     xy=(0.48, 0.12), xycoords='axes fraction', color='royalblue')
        plt.annotate(f'+',
                     xy=(0.63, 0.12), xycoords='axes fraction', color='darkorchid')
        plt.annotate(f'Flex-Rate',
                     xy=(0.66, 0.12), xycoords='axes fraction', color='r')
        plt.annotate(f'Flex-Rate',
                     xy=(0.6, 0.24), xycoords='axes fraction', color='r')
        plt.annotate(f'Flex-Rate',
                     xy=(0.7, 0.49), xycoords='axes fraction', color='r')
        plt.annotate(f'Shannon-Rate',
                     xy=(0.65, 0.9), xycoords='axes fraction', color='limegreen')

        plt.annotate(f'PM-QPSK',
                     xy=(0.03, 0.155), xycoords='axes fraction')
        plt.annotate(f'PM-8-QAM',
                     xy=(0.03, 0.28), xycoords='axes fraction')
        plt.annotate(f'PM-16-QAM',
                     xy=(0.03, 0.53), xycoords='axes fraction')

        plt.show()

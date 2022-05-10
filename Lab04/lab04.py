import random
import matplotlib.pyplot as plt
import math
from scipy.special import erfcinv

from network import Network
from connection import Connection


if __name__ == '__main__':
    BER_t = 1e-3
    Rs = 32
    Bn = 12.5

    N = Network(10)
    N.connect()
    used_paths = list()

    # N.draw()

    """nodes = N.nodes.keys()
    node_list = list()
    connections = list()

    power = 0.001
    for i in range(20):
        node_list.append(random.sample(nodes, 2))
    # finding paths based on best latency:
    for i in node_list:
        connections.append(Connection(i[0], i[1], power))

    used_paths = N.stream(connections)
    path_cnt = 0

    for i in connections:
        print("\nConnection: " + str(i.input + "->" + i.output), end='')

        used_path = 'None'
        if i.snr != 0:
            used_path = used_paths[path_cnt]
            path_cnt += 1
        print("\tBest available latency path: " + used_path)

        print("Latency: " + str(i.latency), end='')
        print("\tSNR: " + str(i.snr))

    # freeing lines
    for i in N.lines.values():
        for j in range(N.number_of_channels):
            i.set_state(j, 1)

    N.route_space.to_csv('used_paths_lat.csv')
    N.reset_route_space()

    # finding paths based on best snr:
    for i in node_list:
        connections.append(Connection(i[0], i[1], power))

    used_paths = N.stream(connections, 'snr')
    path_cnt = 0

    for i in connections:
        print("\nConnection: " + str(i.input + "->" + i.output), end='')

        used_path = 'None'
        if i.snr != 0:
            used_path = used_paths[path_cnt]
            path_cnt += 1
        print("\tBest available SNR path found: " + used_path)

        print("Latency: " + str(i.latency), end='')
        print("\tSNR: " + str(i.snr))

    N.route_space.to_csv('used_paths_snr.csv')

    # test
    print('\nBitrate of path ' + str(used_paths[-1]) + '=' + str(N.calculate_bit_rate(used_paths[-1], 'shannon-rate')))
    print('\nBitrate of path ' + str(used_paths[0]) + '=' + str(N.calculate_bit_rate(used_paths[0], 'flex-rate')))
    print('\nBitrate of path ' + str(used_paths[1]) + '=' + str(N.calculate_bit_rate(used_paths[1], 'flex-rate')))
    print('\nBitrate of path ' + str(used_paths[2]) + '=' + str(N.calculate_bit_rate(used_paths[2], 'flex-rate')))
    print('\nBitrate of path ' + str('ABDE') + '=' + str(N.calculate_bit_rate('ABDE', 'shannon-rate')))"""

    # 2. Plot on the same figure the bit rate curve versus GSNR (in dB) of each
    # transceiver technology.
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
    x2 = 14/3 * ((erfcinv(3/2 * BER_t)) ** 2) * Rs/Bn
    x = (10 * math.log(x1, 10), 10 * math.log(x2, 10))
    y = (100, 100)
    plt.plot(x, y, color='r', linestyle='-')

    # up
    x = (10 * math.log(x2, 10), 10 * math.log(x2, 10))
    y = (100, 200)
    plt.plot(x, y, color='r', linestyle='-')

    # PM-8-QAM (200Gbps)
    x1 = float(x2)
    x2 = 10 * ((erfcinv(8/3 * BER_t)) ** 2) * Rs/Bn
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

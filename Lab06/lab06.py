import random
import matplotlib.pyplot as plt

from classes.network import Network
from classes.connection import Connection


def path_searcher(N, strat, node_list, pn):
    # finding paths based on best gsnr:
    connections = list()
    for i in node_list:
        connections.append(Connection(i[0], i[1]))

    used_paths = N.stream(connections, 'snr')
    path_cnt = 0

    for i in connections:
        print("\nConnection " + strat + ": " + str(i.input + "->" + i.output), end='')

        used_path = 'None'
        if i.snr != 0:
            used_path = used_paths[path_cnt]
            path_cnt += 1
        print("\t\t\tBest available SNR path found: " + used_path)

        print("Latency: " + str(i.latency), end='')
        print("\t\tGSNR: " + str(i.snr))
        print("\t\tBit rate: " + str(i.bit_rate))

    histogram(connections, pn, strat)

    N.route_space.to_csv('used_paths_' + strat + '_gsnr.csv')


def histogram(connections, pn, strat):
    # x = snr and bit-rate
    # y = occurrences
    x_GSNR = list()
    x_Rb = list()
    avg_Rb = 0
    cnt = 0
    capacity = 0

    for i in connections:
        x_GSNR.append(i.snr)
        x_Rb.append(i.bit_rate)
        capacity += i.bit_rate
        cnt += 1
    avg_Rb = capacity/cnt

    plt.subplot(pn)
    plt.hist(x_GSNR, color='mediumturquoise')
    plt.title(strat+' connection')
    plt.xlabel('GSNR')
    plt.ylabel('Occurrences')

    pn += 1
    plt.subplot(pn)
    plt.hist(x_Rb, color='coral')
    plt.title(strat+' connection')
    plt.xlabel('Bit-Rate')


    avg_Rb = round(avg_Rb, 3)
    capacity = capacity/1000
    capacity = round(capacity, 3)

    pn += 1
    plt.subplot(pn)
    plt.axis('off')
    plt.annotate(f'Average Bit-Rate: '+ str(avg_Rb) + ' Gb/s',
                 xy=(0.1, 0.9), xycoords='axes fraction')
    plt.annotate(f'Allocated capacity: ' + str(capacity) + ' Tb/s',
                 xy=(0.1, 0.75), xycoords='axes fraction')


# 5. Run the main that evaluates the distribution of the SNR on a list of
#    100 randomly chosen connections for the three newly provided network
#    description json files and plot the histogram of the accepted connections
#    bit rates calculating the overall average. Also calculate the total capacity
#    allocated into the network. Compare the three results obtained for the
#    three different transceiver strategies.
if __name__ == '__main__':

    pn = 331

    N_fixed = Network(10, 'json_files/nodes_fixed.json')
    N_flex = Network(10, 'json_files/nodes_flex.json')
    N_shannon = Network(10, 'json_files/nodes_shannon.json')
    N_fixed.connect()
    N_flex.connect()
    N_shannon.connect()

    # N.draw()

    nodes = N_fixed.nodes.keys()
    node_list = list()

    for i in range(100):
        node_list.append(random.sample(nodes, 2))

    plt.subplots(3, 3, figsize=(9, 7))

    # Fixed-rate
    path_searcher(N_fixed, 'fixed_rate', node_list, pn)
    pn += 3

    # Flex-rate
    path_searcher(N_flex, 'flex_rate', node_list, pn)
    pn += 3

    # Shannon
    path_searcher(N_shannon, 'shannon', node_list, pn)

    # plt.tight_layout()
    plt.subplots_adjust(hspace=0.7)
    plt.show()

    # N_fixed.graph()

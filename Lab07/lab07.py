import matplotlib.pyplot as plt

from classes.network import Network


def path_searcher(N, strat, pn, nodes, req):
    # finding paths based on best gsnr:

    T = list(list())
    for i in nodes:
        row = list()
        for j in nodes:
            if i == j:
                row.append(0)
            else:
                row.append(req)
        T.append(row)

    connections, used_paths = N.manage_traffic(T, nodes)
    # used_paths = N.stream(connections, T, nodes, 'snr')
    path_cnt = 0
    for i in connections:
        print("\nConnection " + strat + ": " + str(i.input + "->" + i.output), end='')

        used_path = 'None'
        if i.snr != 0:
            used_path = used_paths[path_cnt]
            path_cnt += 1
        print("\t\t\tBest available SNR path found: " + used_path)

        if i.latency:
            print("Latency: " + str(round(i.latency, 7)) + " [s]", end='')
        else:
            print("Latency: " + str(i.latency), end='')
        print("\t\t\t\tGSNR: " + str(round(i.snr, 7)) + " [dB]")
        print("\t\t\tBit rate: " + str(round(i.bit_rate, 3)) + " [Gb/s]")

    print('\n A  B  C  D  E  F')
    for i in range(len(T)):
        print(T[i])

    histogram(connections, pn, strat)

    N.route_space.to_csv('used_paths_' + strat + '_gsnr.csv')


def histogram(connections, pn, strat):
    # x = snr and bit-rate
    # y = occurrences
    x_GSNR = list()
    x_Rb = list()
    avg_GSNR = 0
    cnt = 0
    capacity = 0

    for i in connections:
        x_GSNR.append(i.snr)
        avg_GSNR += i.snr
        x_Rb.append(i.bit_rate)
        capacity += i.bit_rate
        cnt += 1
    avg_Rb = capacity/cnt
    avg_GSNR = avg_GSNR/cnt

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

    avg_GSNR = round(avg_GSNR, 3)
    avg_Rb = round(avg_Rb, 3)
    capacity = capacity/1000
    capacity = round(capacity, 3)

    pn += 1
    plt.subplot(pn)
    plt.axis('off')
    plt.annotate(f'Average GSNR: ' + str(avg_GSNR) + ' dB',
                 xy=(0.1, 0.9), xycoords='axes fraction')
    plt.annotate(f'Average Bit-Rate: '+ str(avg_Rb) + ' Gb/s',
                 xy=(0.1, 0.75), xycoords='axes fraction')
    plt.annotate(f'Allocated capacity: ' + str(capacity) + ' Tb/s',
                 xy=(0.1, 0.6), xycoords='axes fraction')


if __name__ == '__main__':

    pn = 331

    N_fixed = Network(10, 'json_files/nodes_fixed.json')
    N_flex = Network(10, 'json_files/nodes_flex.json')
    N_shannon = Network(10, 'json_files/nodes_shannon.json')
    N_fixed.connect()
    N_flex.connect()
    N_shannon.connect()

    # N.draw()

    nodes = list(N_fixed.nodes.keys())
    # old random connections list generation
    """node_list = list()

    for i in range(100):
        node_list.append(random.sample(nodes, 2))"""

    plt.subplots(3, 3, figsize=(9, 7))

    # Fixed-rate
    path_searcher(N_fixed, 'fixed_rate', pn, nodes, 300)
    pn += 3

    # Flex-rate
    path_searcher(N_flex, 'flex_rate', pn, nodes, 600)
    pn += 3

    # Shannon
    path_searcher(N_shannon, 'shannon', pn, nodes, 1500)

    # plt.tight_layout()
    plt.subplots_adjust(hspace=0.7)
    plt.show()

    # N_fixed.graph()

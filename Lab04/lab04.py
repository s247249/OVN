import random

from network import Network
from connection import Connection


if __name__ == '__main__':
    N = Network(10)
    N.connect()
    used_paths = list()

    # N.draw()

    nodes = N.nodes.keys()
    node_list = list()
    connections = list()

    power = 0.001
    for i in range(100):
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
    print('\nBitrate of path ' + str('ABDE') + '=' + str(N.calculate_bit_rate('ABDE', 'shannon-rate')))

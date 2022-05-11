import random

from network import Network
from connection import Connection


# 5. Run the main that evaluates the distribution of the SNR on a list of
#    100 randomly chosen connections for the three newly provided network
#    description json files and plot the histogram of the accepted connections
#    bit rates calculating the overall average. Also calculate the total capacity
#    allocated into the network. Compare the three results obtained for the
#    three different transceiver strategies.
if __name__ == '__main__':

    N_fixed = Network(10, 'nodes_fixed.json')
    N_flex = Network(10, 'nodes_flex.json')
    N_shannon = Network(10, 'nodes_shannon.json')
    N_fixed.connect()
    N_flex.connect()
    N_shannon.connect()
    used_paths_fixed = list()
    used_paths_flex = list()
    used_paths_shannon = list()

    # N.draw()

    nodes = N_fixed.nodes.keys()
    node_list = list()

    power = 0.001
    for i in range(100):
        node_list.append(random.sample(nodes, 2))

    # Fixed-rate
    # finding paths based on best latency:
    connections = list()
    for i in node_list:
        connections.append(Connection(i[0], i[1], power))

    used_paths_fixed = N_fixed.stream(connections)
    path_cnt = 0

    for i in connections:
        print("\nFixed-rate connection: " + str(i.input + "->" + i.output), end='')

        used_path = 'None'
        if i.snr != 0:
            used_path = used_paths_fixed[path_cnt]
            path_cnt += 1
        print("\t\t\tBest available latency path: " + used_path)

        print("Latency: " + str(i.latency), end='')
        print("\t\tSNR: " + str(i.snr))
        print("\t\tBit rate: " + str(i.bit_rate))

    # freeing lines
    for i in N_fixed.lines.values():
        for j in range(N_fixed.number_of_channels):
            i.set_state(j, 1)

    N_fixed.route_space.to_csv('used_paths_fixed_lat.csv')
    N_fixed.reset_route_space()

    # finding paths based on best snr:
    connections = list()
    for i in node_list:
        connections.append(Connection(i[0], i[1], power))

    used_paths_fixed = N_fixed.stream(connections, 'snr')
    path_cnt = 0

    for i in connections:
        print("\nFixed-rate connection: " + str(i.input + "->" + i.output), end='')

        used_path = 'None'
        if i.snr != 0:
            used_path = used_paths_fixed[path_cnt]
            path_cnt += 1
        print("\t\t\tBest available SNR path found: " + used_path)

        print("Latency: " + str(i.latency), end='')
        print("\t\tSNR: " + str(i.snr))
        print("\t\tBit rate: " + str(i.bit_rate))

    N_fixed.route_space.to_csv('used_paths_fixed_snr.csv')

    # Flex-rate
    # finding paths based on best latency:
    connections = list()
    for i in node_list:
        connections.append(Connection(i[0], i[1], power))

    used_paths_flex = N_flex.stream(connections)
    path_cnt = 0

    for i in connections:
        print("\nFlex-rate connection: " + str(i.input + "->" + i.output), end='')

        used_path = 'None'
        if i.snr != 0:
            used_path = used_paths_flex[path_cnt]
            path_cnt += 1
        print("\t\t\tBest available latency path: " + used_path)

        print("Latency: " + str(i.latency), end='')
        print("\t\tSNR: " + str(i.snr))
        print("\t\tBit rate: " + str(i.bit_rate))

    # freeing lines
    for i in N_flex.lines.values():
        for j in range(N_flex.number_of_channels):
            i.set_state(j, 1)

    N_flex.route_space.to_csv('used_paths_flex_lat.csv')
    N_flex.reset_route_space()

    # finding paths based on best snr:
    connections = list()
    for i in node_list:
        connections.append(Connection(i[0], i[1], power))

    used_paths_flex = N_flex.stream(connections, 'snr')
    path_cnt = 0

    for i in connections:
        print("\nFlex-rate connection: " + str(i.input + "->" + i.output), end='')

        used_path = 'None'
        if i.snr != 0:
            used_path = used_paths_flex[path_cnt]
            path_cnt += 1
        print("\t\t\tBest available SNR path found: " + used_path)

        print("Latency: " + str(i.latency), end='')
        print("\t\tSNR: " + str(i.snr))
        print("\t\tBit rate: " + str(i.bit_rate))

    N_flex.route_space.to_csv('used_paths_flex_snr.csv')

    # Shannon
    # finding paths based on best latency:
    connections = list()
    for i in node_list:
        connections.append(Connection(i[0], i[1], power))

    used_paths_shannon = N_shannon.stream(connections)
    path_cnt = 0

    for i in connections:
        print("\nShannon connection: " + str(i.input + "->" + i.output), end='')

        used_path = 'None'
        if i.snr != 0:
            used_path = used_paths_shannon[path_cnt]
            path_cnt += 1
        print("\t\t\tBest available latency path: " + used_path)

        print("Latency: " + str(i.latency), end='')
        print("\t\tSNR: " + str(i.snr))
        print("\t\tBit rate: " + str(i.bit_rate))

    # freeing lines
    for i in N_shannon.lines.values():
        for j in range(N_shannon.number_of_channels):
            i.set_state(j, 1)

    N_shannon.route_space.to_csv('used_paths_shannon_lat.csv')
    N_shannon.reset_route_space()

    # finding paths based on best snr:
    connections = list()
    for i in node_list:
        connections.append(Connection(i[0], i[1], power))

    used_paths_shannon = N_shannon.stream(connections, 'snr')
    path_cnt = 0

    for i in connections:
        print("\nShannon connection: " + str(i.input + "->" + i.output), end='')

        used_path = 'None'
        if i.snr != 0:
            used_path = used_paths_shannon[path_cnt]
            path_cnt += 1
        print("\t\t\tBest available SNR path found: " + used_path)

        print("Latency: " + str(i.latency), end='')
        print("\t\tSNR: " + str(i.snr))
        print("\t\tBit rate: " + str(i.bit_rate))

    N_shannon.route_space.to_csv('used_paths_shannon_snr.csv')
    N_fixed.graph()

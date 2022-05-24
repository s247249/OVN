import random

from classes.network import Network
from classes.connection import Connection


def path_searcher(N, strat, node_list):
    # finding paths based on best latency:
    used_paths = list()
    connections = list()
    for i in node_list:
        # REMOVED POWER
        connections.append(Connection(i[0], i[1]))

    used_paths = N.stream(connections)
    path_cnt = 0

    for i in connections:
        print("\nConnection " + strat + ": " + str(i.input + "->" + i.output), end='')

        used_path = 'None'
        if i.snr != 0:
            used_path = used_paths[path_cnt]
            path_cnt += 1
        print("\t\t\tBest available latency path: " + used_path)

        print("Latency: " + str(i.latency), end='')
        print("\t\tSNR: " + str(i.snr))
        print("\t\tBit rate: " + str(i.bit_rate))

    # freeing lines
    for i in N.lines.values():
        for j in range(N.number_of_channels):
            i.set_state(j, 1)

    N.route_space.to_csv('used_paths_' + strat + '_lat.csv')
    N.reset_route_space()

    # finding paths based on best snr:
    connections = list()
    for i in node_list:
        # REMOVED POWER
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
        print("\t\tSNR: " + str(i.snr))
        print("\t\tBit rate: " + str(i.bit_rate))

    N.route_space.to_csv('used_paths_' + strat + '_snr.csv')


if __name__ == '__main__':

    N_fixed = Network(10, 'json_files/nodes_fixed.json')
    N_flex = Network(10, 'json_files/nodes_flex.json')
    N_shannon = Network(10, 'json_files/nodes_shannon.json')
    N_fixed.connect()
    N_flex.connect()
    N_shannon.connect()
    """used_paths_fixed = list()
    used_paths_flex = list()
    used_paths_shannon = list()"""

    # N.draw()

    nodes = N_fixed.nodes.keys()
    node_list = list()

    # power = 0.001
    for i in range(100):
        node_list.append(random.sample(nodes, 2))

    # Fixed-rate
    """# finding paths based on best latency:
    connections = list()
    for i in node_list:
        # REMOVED POWER
        connections.append(Connection(i[0], i[1]))

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
        # REMOVED POWER
        connections.append(Connection(i[0], i[1]))

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

    N_fixed.route_space.to_csv('used_paths_fixed_snr.csv')"""
    path_searcher(N_fixed, 'fixed_rate', node_list)

    # Flex-rate
    """# finding paths based on best latency:
    connections = list()
    for i in node_list:
        # REMOVED POWER
        connections.append(Connection(i[0], i[1]))

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
        # REMOVED POWER
        connections.append(Connection(i[0], i[1]))

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

    N_flex.route_space.to_csv('used_paths_flex_snr.csv')"""
    path_searcher(N_flex, 'flex_rate', node_list)

    # Shannon
    """# finding paths based on best latency:
    connections = list()
    for i in node_list:
        # REMOVED POWER
        connections.append(Connection(i[0], i[1]))

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
        # REMOVED POWER
        connections.append(Connection(i[0], i[1]))

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

    N_shannon.route_space.to_csv('used_paths_shannon_snr.csv')"""
    path_searcher(N_shannon, 'shannon', node_list)

    N_fixed.graph()

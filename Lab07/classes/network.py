import json
import math
import matplotlib.pyplot as plt
import pandas as pd

from .node import Node
from .line import Line
from .signal_information import Lightpath
from .added_methods.network_path_finder import PathFind
from .added_methods.lab04_network import Network4
from .added_methods.lab06_network import Network6
from .added_methods.lab07_network import Network7


class Network(PathFind, Network4, Network6, Network7):
    def __init__(self, number_of_channels, file_name="../Lab01/nodes.json"):
        self._nodes = {}
        self._lines = {}
        self._weighted_paths = pd.read_csv("../Lab01/Network.csv")
        self._number_of_channels = number_of_channels

        rf = open(file_name, "r")
        py_dict = dict(json.load(rf))
        node_dict = {}
        labels = list()
        # node creation
        for i in py_dict:
            labels.append(i)
        cnt = 0
        for i in py_dict.values():
            node_dict['label'] = str(labels[cnt])
            cnt += 1
            node_dict['position'] = tuple(i['position'])
            node_dict['connected_nodes'] = list(i['connected_nodes'])
            if 'transceiver' in i:
                node_dict['transceiver'] = str(i['transceiver'])
            else:
                node_dict['transceiver'] = 'fixed-rate'
            self._nodes[node_dict['label']] = Node(dict(node_dict))

        # line creation
        for i in self._nodes.values():
            for j in i.connected_nodes:
                label = str(i.label)+str(j)
                x = abs(i.position[0] - self._nodes[j].position[0])
                y = abs(i.position[1] - self._nodes[j].position[1])
                float_tuple = (x, y)
                length = math.sqrt(float_tuple[0]**2 + float_tuple[1]**2)
                self._lines[label] = Line(label, length, number_of_channels)

        route_space_dict = {'Path': list()}
        for i in self.nodes.keys():
            for j in self.nodes:
                if i != j:
                    route_space_dict['Path'] += self.find_paths(i, j)

        for i in range(number_of_channels):
            for j in range(len(route_space_dict['Path'])):
                route_space_dict[str(i + 1)] = 1
        self._route_space = pd.DataFrame(route_space_dict)

        # 1. Add a new attribute to the class Network called logger which is a pandas
        #    dataframe, initialize as empty. It must have the following labels: epoch
        #    time (float), path (string), channel ID (string), bit rate (integer).
        logger_dict = {'Epoch Time': float(), 'Path': str(), 'Channel ID': str(), 'Bit Rate': int()}
        self._logger = pd.DataFrame(logger_dict, index=[0])

    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    @property
    def weighted_paths(self):
        return self._weighted_paths

    @property
    def number_of_channels(self):
        return self._number_of_channels

    @property
    def route_space(self):
        return self._route_space

    @property
    def logger(self):
        return self._logger

    def reset_route_space(self):
        for i in range(self.number_of_channels):
            self.route_space[str(i + 1)] = int(1)

    def connect(self):
        for i in self.nodes.values():
            for j in self.lines.values():
                chars = list(str(j.label))
                if str(i.label) == chars[0]:
                    i.set_successive(j)
                elif str(i.label) == chars[1]:
                    j.set_successive(i)

    def propagate(self, signal_information):
        spectral_info = {}
        first_node = str(signal_information.path[0])
        self.nodes[first_node].propagate(signal_information)

        spectral_info['signal_power'] = signal_information.signal_power
        spectral_info['noise_power'] = signal_information.noise_power
        spectral_info['latency'] = signal_information.latency
        return spectral_info

    def probe(self, signal_information):
        spectral_info = {}
        first_node = str(signal_information.path[0])
        self.nodes[first_node].probe(signal_information)

        spectral_info['signal_power'] = signal_information.signal_power
        spectral_info['noise_power'] = signal_information.noise_power
        spectral_info['latency'] = signal_information.latency
        return spectral_info

    def draw(self):
        connections = {}
        i_coords = list()
        j_coords = list()
        x_coords = tuple()
        y_coords = tuple()

        for i in self.nodes.values():
            connections[i.label] = i.connected_nodes

        plt.figure()
        for i in connections.keys():
            for j in connections.keys():
                if str(j) in connections[i]:
                    i_coords = list(self.nodes[i].position)
                    j_coords = list(self.nodes[j].position)
                    x_coords = (float(i_coords[0]), float(j_coords[0]))
                    y_coords = (float(i_coords[1]), float(j_coords[1]))
                    plt.plot(x_coords, y_coords, color='#00cc00', marker='o', markerfacecolor='k', linestyle='-')

        for i in self.nodes.values():
            plt.annotate(i.label, i.position, fontsize=15)

        plt.show()

    def stream(self, connection, latency_or_snr='latency'):
        p = ''

        if latency_or_snr == 'latency':
            p_list = self.find_best_latency(connection.input, connection.output)
        elif latency_or_snr == 'snr':
            p_list = self.find_best_snr(connection.input, connection.output)
        else:
            print("wrong argument for 'latency_or_snr'\nWrite either 'latency' or 'snr'")
            return

        if not p_list:
            connection.latency = None
            connection.snr = 0
            connection.bit_rate = 0
        else:
            channel = p_list.pop()
            # generate return string p
            for j in p_list:
                p += j

            strategy = str(self.nodes[p_list[0]].transceiver)

            s = Lightpath(connection.signal_power, channel)

            # 4. Modify the stream() method of the class Network in order to include this
            #    feature in the evaluation of the path availability.
            """# Note: I don't check line availability, I just check the availability of the route_space.
            #       I do that because if the route_space has been occupied, it means that at least 1 line
            #       has that channel occupied itself, so I don't need to check all the lines in a path"""

            # occupy lines
            for j in range(0, len(p_list) - 1):
                self.lines[str(p_list[j] + p_list[j+1])].state[channel - 1] = 0
                """# I can, however, still update the attribute
                flag = 0
                for ch in range(self.number_of_channels):
                    if self.lines[str(p_list[j] + p_list[j + 1])].state[ch] == 1:
                        flag = 1
                if not flag:
                    self.lines[str(p_list[j] + p_list[j + 1])].in_service = 0"""

            s.path = list(p_list)

            self.propagate(s)
            Rb = self.calculate_bit_rate(s, strategy)
            if Rb == 0:
                p = ''
                connection.latency = None
                connection.snr = 0
                connection.bit_rate = Rb
            else:
                # occupy channel for specific path
                self.route_space.loc[self.route_space['Path'] == p, str(channel)] = 0

                # find other paths to occupy:
                # extract lines to find from selected path
                to_find = list()
                for ind in range(len(p_list) - 1):
                    to_find.append(str(p_list[ind] + p_list[ind + 1]))
                # extract list of paths from pandas dataframe
                for ind in range(len(to_find)):
                    to_change = [a for a in self.route_space['Path'] if to_find[ind] in a]
                # update dataframe using list of paths
                for ind in range(len(to_change)):
                    self.route_space.loc[self.route_space['Path'] == to_change[ind], str(channel)] = 0

                # The update of the logger is performed immediately after the update of the routing-space.

                connection.bit_rate = Rb
                connection.signal_power = s.signal_power
                connection.latency = s.latency

                """connection.snr = 10 * math.log(s.signal_power / s.noise_power, 10)"""
                connection.snr = s.GSNR_tot

        return p


import json
import math
import matplotlib.pyplot as plt
import pandas as pd

from node import Node
from line import Line
from signal_information import Lightpath
from lab04_network_methods import Network4 as net4


class Network:
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

        route_space_dict = {}
        route_space_dict['Path'] = list()
        for i in self.nodes.keys():
            for j in self.nodes:
                if i != j:
                    route_space_dict['Path'] += self.find_paths(i, j)

        for i in range(number_of_channels):
            for j in range(len(route_space_dict['Path'])):
                route_space_dict[str(i + 1)] = 1
        self._route_space = pd.DataFrame(route_space_dict)

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

    def recursive_find_paths(self, current_node, final_node, wip_path, path_list):
        path_str = ""

        if current_node == final_node:
            for i in range(len(wip_path)):
                path_str += str(wip_path[i])
            if path_str not in path_list:
                path_list.append(path_str)
            else:
                return

        for i in self.nodes.keys():
            if len(wip_path) == 0:
                return
            if i not in wip_path:
                if i in self.nodes[current_node].connected_nodes:
                    wip_path.append(i)
                    self.recursive_find_paths(i, final_node, wip_path, path_list)
                    wip_path.pop(-1)

    def find_paths(self, starting_node, final_node):
        nodes_dict = dict(self.nodes)
        del nodes_dict[starting_node]

        self.connect()

        path_list = list(str())
        wip_path = [starting_node]
        self.recursive_find_paths(starting_node, final_node, wip_path, path_list)
        return path_list

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

    def find_best_snr(self, in_node, out_node):
        best_snr = 0
        cnt = 0
        best_path = list()
        flag = 1

        for i in self.weighted_paths['Routes']:
            if i == str(in_node + "->" + out_node):

                # free lines check
                path = self.weighted_paths['Path'][cnt]
                path_list = list(path)
                channel = int()
                flag = 1
                for k in range(1, self.number_of_channels + 1):
                    if int(self.route_space.loc[self.route_space['Path'] == path, str(k)]) != 0:
                        channel = k
                        flag = 0
                        break

                # if I've found no channels, check the next route
                if flag:
                    cnt += 1
                    flag = 0
                    continue

                if self.weighted_paths['SNR (dB)'][cnt] > best_snr:
                    best_snr = self.weighted_paths['SNR (dB)'][cnt]
                    best_path = list(self.weighted_paths['Path'][cnt])
                    best_path.append(channel)

            cnt += 1

        return best_path

    def find_best_latency(self, in_node, out_node):
        best_lat = -1
        cnt = 0
        best_path = list()

        for i in self.weighted_paths['Routes']:
            if i == str(in_node + "->" + out_node):

                # free lines check
                path = self.weighted_paths['Path'][cnt]
                path_list = list(path)
                channel = int()
                flag = 1
                for k in range(1, self.number_of_channels + 1):
                    if int(self.route_space.loc[self.route_space['Path'] == path, str(k)]) != 0:
                        channel = k
                        flag = 0
                        break

                # if I've found no channels, check the next route
                if flag:
                    cnt += 1
                    flag = 0
                    continue

                if (self.weighted_paths['Latency (s)'][cnt] < best_lat) or (best_lat == -1):
                    best_lat = self.weighted_paths['Latency (s)'][cnt]
                    best_path = list(self.weighted_paths['Path'][cnt])
                    if channel != 0:
                        best_path.append(channel)

            cnt += 1

        return best_path

    # 4. Modify the stream() method of the Network class that has to call the
    #    calculate_bit_rate(path, strategy) once the path for the connection
    #    is given and using the transceiver attribute value of the first node in the
    #    path. If the path does not reach the minimum GSNR requirement for the
    #    specified transceiver strategy (zero bit rate case), the connection has to be
    #    rejected. Add the attribute bit rate to the Connection class that stores
    #    the assigned bit rate Rb.
    def stream(self, connections, latency_or_snr='latency'):
        used_paths = list()

        all_paths = list()
        for i in self.route_space['Path']:
            all_paths.append(str(i))

        for i in connections:
            if latency_or_snr == 'latency':
                p_list = self.find_best_latency(i.input, i.output)
            elif latency_or_snr == 'snr':
                p_list = self.find_best_snr(i.input, i.output)
            else:
                print("wrong argument for 'latency_or_snr'\nWrite either 'latency' or 'snr'")
                return

            if not p_list:
                i.latency = None
                i.snr = 0
                i.bit_rate = 0
            else:
                channel = p_list.pop()
                p = ''
                for j in p_list:
                    p += j

                strategy = str(self.nodes[p_list[0]].transceiver)
                Rb = self.calculate_bit_rate(p, strategy)
                if Rb == 0:
                    i.latency = None
                    i.snr = 0
                    i.bit_rate = Rb
                else:
                    s = Lightpath(i.signal_power, channel)
                    # occupy lines
                    for j in range(0, len(p_list) - 1):
                        self.lines[str(p_list[j] + p_list[j+1])].state[channel - 1] = 0

                    s.path = p_list

                    # occupy channel for specific path
                    self.route_space.loc[self.route_space['Path'] == p, str(channel)] = 0

                    # find other paths to occupy:
                    # extract lines to find from selected path
                    to_find = list()
                    for ind in range(len(p_list) - 1):
                        to_find.append(str(p_list[ind] + p_list[ind + 1]))
                    # extract list of paths from pandas dataframe
                    to_change = list()
                    for ind in range(len(to_find)):
                        to_change = [a for a in self.route_space['Path'] if to_find[ind] in a and a not in to_change]
                        # update dataframe using list of paths
                        for ind1 in range(len(to_change)):
                            self.route_space.loc[self.route_space['Path'] == to_change[ind1], str(channel)] = 0

                    self.propagate(s)
                    i.latency = s.latency

                    i.snr = 10 * math.log(s.signal_power/s.noise_power, 10)

                    i.bit_rate = Rb

                    # for print purposes
                    used_paths.append(p)

        return used_paths

    def calculate_bit_rate(self, path, strategy):
        return net4.calculate_bit_rate(self, path, strategy)

    def graph(self):
        net4.graph(self)
import json
import math
import matplotlib.pyplot as plt
import pandas as pd
import random


# 3. Define a new method in all the elements that propagate a SignalInforma-
#    tion without occupying any line. This new method, that can be called
#    probe, must be used to create the weighted graph instead of using the
#    propagate method.
class SignalInformation:
    def __init__(self, signal_power):
        self._signal_power = float(signal_power)
        self._noise_power = float(0)
        self._latency = float(0)
        self._path = list()

    @property
    def signal_power(self):
        return self._signal_power

    @property
    def noise_power(self):
        return self._noise_power

    @property
    def latency(self):
        return self._latency

    @property
    def path(self):
        return self._path

    @signal_power.setter
    def signal_power(self, signal_power):
        self._signal_power = signal_power

    @noise_power.setter
    def noise_power(self, noise_power):
        self._noise_power = noise_power

    @latency.setter
    def latency(self, latency):
        self._latency = latency

    @path.setter
    def path(self, path):
        self._path = path

    def update_signal_power(self, signal_power):
        sp = self._signal_power + signal_power
        self.signal_power += sp

    def update_noise_power(self, noise_power):
        np = self._noise_power + noise_power
        self.noise_power += np

    def update_latency(self, latency):
        self.latency += latency

    def update_path(self):
        del self.path[0]
        if len(self.path) > 0:
            return self.path[0]
        else:
            return 0


# 1. Define the class Lightpath as an extension of the class SignalInforma-
#    tion. Beside the latter list of attributes, an instance of Lightpath has
#    to include an attribute channel which is an integer and indicates which
#    frequency slot the signal occupies when is propagated.
class Lightpath(SignalInformation):
    def __init__(self, signal_power, channel):
        super().__init__(signal_power)
        self._channel = channel

    @property
    def channel(self):
        return self._channel


class Node:
    def __init__(self, py_dict):
        self._label = str(py_dict['label'])
        self._position = tuple(py_dict['position'])
        self._connected_nodes = list(py_dict['connected_nodes'])
        self._successive = dict()

    @property
    def label(self):
        return self._label

    @property
    def position(self):
        return self._position

    @property
    def connected_nodes(self):
        return self._connected_nodes

    @property
    def successive(self):
        return self._successive

    @label.setter
    def label(self, label):
        self._label = label

    @position.setter
    def position(self, position):
        self._position = position

    @connected_nodes.setter
    def connected_nodes(self, nodes):
        self._connected_nodes = nodes

    def set_successive(self, line):
        self._successive[line.label] = line

    def propagate(self, signal):
        next_node = str(signal.update_path())
        if next_node != "0":
            self.successive[self.label + next_node].propagate(signal)

    def probe(self, signal):
        next_node = str(signal.update_path())
        if next_node != "0":
            self.successive[self.label + next_node].probe(signal)


# 2. Modify the attribute state of the class Line; it has to be a list of strings
#    that indicate the occupancy of each channel. Moreover, modify the method
#    propagate accordingly.
class Line:
    def __init__(self, label, length, number_of_channels):
        self._label = label
        self._length = length
        self._successive = dict()
        self._state = list()

        for i in range(number_of_channels):
            self._state.append(1)

    @property
    def label(self):
        return self._label

    @property
    def length(self):
        return self._length

    @property
    def successive(self):
        return self._successive

    @property
    def state(self):
        return self._state

    @label.setter
    def label(self, label):
        self._label = label

    @length.setter
    def length(self, length):
        self._length = length

    def set_state(self, index, state):
        self._state[index] = state

    def set_successive(self, node):
        self._successive[node.label] = node

    def latency_generation(self):
        return float(self._length / (3e8 * 2/3))

    def noise_generation(self, signal_power):
        return float(1e-9 * signal_power * self.length)

    def propagate(self, signal):
        latency = self.latency_generation()
        noise = self.noise_generation(signal.signal_power)
        signal.update_latency(latency)
        signal.update_noise_power(noise)
        for i in self.successive.values():
            i.propagate(signal)

    def probe(self, signal):
        latency = self.latency_generation()
        noise = self.noise_generation(signal.signal_power)
        signal.update_latency(latency)
        signal.update_noise_power(noise)
        for i in self.successive.values():
            i.probe(signal)


# 4. Define the attribute route_space in the class Network. It has to be a
#    pandas dataframe that for all the possible paths describe the availability
#    for each channel.
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

    # 5. Modify the methods find best snr() and find best latency() in the
    #    class Network such that they manage the channel occupancy.
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
            else:
                channel = p_list.pop()
                p = ''
                for j in p_list:
                    p += j

                s = Lightpath(i.signal_power, channel)
                # occupy lines
                for j in range(0, len(p_list) - 1):
                    self.lines[str(p_list[j] + p_list[j+1])].state[channel - 1] = 0

                s.path = p_list
                # 6. Modify the methods propagate and stream in the class Network that
                #    should use and update the attribute route_space in order to consider the
                #    channel occupancy for any path.
                self.route_space.loc[self.route_space['Path'] == p, str(channel)] = 0

                to_find = list()
                for ind in range(len(p_list)-1):
                    to_find.append(str(p_list[ind] + p_list[ind + 1]))

                for ind in range(len(to_find)):
                    to_change = [a for a in self.route_space['Path'] if to_find[ind] in a]

                for ind in range(len(to_change)):
                    self.route_space.loc[self.route_space['Path'] == to_change[ind], str(channel)] = 0

                self.propagate(s)
                i.latency = s.latency

                i.snr = 10 * math.log(s.signal_power/s.noise_power, 10)

                # for print purposes
                used_paths.append(p)

        return used_paths


class Connection:
    def __init__(self, input, output, signal_power):
        self._input = str(input)
        self._output = str(output)
        self._signal_power = float(signal_power)
        self._latency = float(0)
        self._snr = float(0)

    @property
    def input(self):
        return self._input

    @property
    def output(self):
        return self._output

    @property
    def signal_power(self):
        return self._signal_power

    @property
    def latency(self):
        return self._latency

    @property
    def snr(self):
        return self._snr

    @latency.setter
    def latency(self, latency):
        self._latency = latency

    @snr.setter
    def snr(self, snr):
        self._snr = snr


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

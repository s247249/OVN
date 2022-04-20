import json
import math
import matplotlib.pyplot as plt
import pandas as pd


class SignalInformation:
    def __init__(self, signal_power, path=list(), noise_power=0, latency=0):
        self._signal_power = float(signal_power)
        self._noise_power = float(noise_power)
        self._latency = float(latency)
        self._path = path

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
        l = self._latency + latency
        self.latency += l

    def update_path(self):
        del self.path[0]
        if len(self.path) > 0:
            return self.path[0]
        else:
            return 0


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


class Line:
    def __init__(self, label, length):
        self._label = label
        self._length = length
        self._successive = dict()

    @property
    def label(self):
        return self._label

    @property
    def length(self):
        return self._length

    @property
    def successive(self):
        return self._successive

    @label.setter
    def label(self, label):
        self._label = label

    @length.setter
    def length(self, length):
        self._length = length

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


class Network:
    def __init__(self, file_name="../Lab01/nodes.json"):
        self._nodes = {}
        self._lines = {}
        # 1. Set the dataframe constructed in exercise 5 of Lab 3 as an attribute of the
        #    network called 'weighted paths'.
        self._weighted_paths = pd.read_csv("../Lab01/Network.csv")

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
                self._lines[label] = Line(label, length)

    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    @property
    def weighted_paths(self):
        return self._weighted_paths

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

    # 2. Define a method find best snr() in the class Network that, given a
    #    pair of input and output nodes, returns the path that connects the two
    #    nodes with the best (highest) signal to noise ratio introduced by the signal
    #    propagation.
    def find_best_snr(self, in_node, out_node):
        best_snr = 0
        cnt = 0

        for i in self.weighted_paths['Routes']:

            if i == str(in_node + "->" + out_node):
                if self.weighted_paths['SNR (dB)'][cnt] > best_snr:
                    best_snr = self.weighted_paths['SNR (dB)'][cnt]
                    best_path = self.weighted_paths['Path'][cnt]
            cnt += 1

        return best_path

    # 3. Define a method find best latency() in the class Network that, given
    #    a pair of input and output nodes, returns the path that connects the two
    #    nodes with the best (lowest) latency introduced by the signal propagation.
    def find_best_latency(self, in_node, out_node):
        best_lat = -1
        cnt = 0

        for i in self.weighted_paths['Routes']:

            if i == str(in_node + "->" + out_node):
                if (self.weighted_paths['Latency (s)'][cnt] < best_lat) or (best_lat == -1):
                    best_lat = self.weighted_paths['Latency (s)'][cnt]
                    best_path = self.weighted_paths['Path'][cnt]
            cnt += 1

        return best_path


# 4. Define the class Connection that has the attributes:
#    • input: string
#    • output: string
#    • signal power: float
#    • latency: float
#    • snr: float
#    The attributes latency and snr have to be initialized to zero.
class Connection:
    def __init__(self, input, output, signal_power):
        self._input = str(input)
        self._output = str(output)
        self._signal_power = float(signal_power)
        self._latency = float(0)
        self._snr = float(0)


if __name__ == '__main__':
    N = Network()

    # Testing 1, 2 and 3
    n1 = 'B'
    n2 = 'C'
    snr_path = N.find_best_snr(n1, n2)
    latency_path = N.find_best_latency(n1, n2)
    print("Path from %s to %s with the best SNR: %s" % (n1, n2, snr_path))
    print("Path from %s to %s with the best latency: %s" % (n1, n2, latency_path))

    # Testing 3
    C = Connection('A', 'B', 3.5)
    print(C._input)

    # N.draw()


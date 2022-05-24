# 3. Add the attribute transceiver to the class Node. This attribute can
#    be fixed-rate, flex-rate, shannon and must be read from the network
#    description json file. If the transceiver is not provided in the description
#    file, it has to be set as fixed-rate.
class Node:
    def __init__(self, py_dict):
        self._label = str(py_dict['label'])
        self._position = tuple(py_dict['position'])
        self._connected_nodes = list(py_dict['connected_nodes'])
        self._successive = dict()
        self._transceiver = str(py_dict['transceiver'])

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

    @property
    def transceiver(self):
        return self._transceiver

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

    # 3. Modify the method propagate of the class Node in order to set for each
    #    line the optimal launch power.
    def propagate(self, signal):
        next_node = str(signal.update_path())
        if next_node != "0":
            self.successive[self.label + next_node].propagate(signal)

    def probe(self, signal):
        next_node = str(signal.update_path())
        if next_node != "0":
            self.successive[self.label + next_node].probe(signal)

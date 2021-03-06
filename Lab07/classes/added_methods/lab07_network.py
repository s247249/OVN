import pandas as pd


class Network7:
    # 2. Add a new method to the class Network called update logger() that just
    #    add a series with the mentioned labels to the logger with the information
    #    related to the current allocated connection. The update of the logger is
    #    performed immediately after the update of the routing-space.
    def update_logger(self, epoch_time, path, channel_ID, bit_rate):
        row_dict = {'Epoch Time': epoch_time, 'Path': path, 'Channel ID': channel_ID, 'Bit Rate': bit_rate}
        logger_row = pd.DataFrame(row_dict, index=[0])
        self._logger.append(logger_row)

    # 5. Add a new method to the class Network called strong_failure() which
    #    allows to emulate a fiber cut on a link. This method receives a single
    #    label related to a line instance and sets the attribute in service of the
    #    corresponding object to 0.
    def strong_failure(self, label):
        self.lines[label].in_service = 0

    # 6. Add a new method to the class Network called traffic recovery() which
    #    checks if there are mismatches between the traffic matrix, the routing-
    #    space and the status of the network starting from the information con-
    #    tained in the logger and restores the correct information.
    def traffic_recovery(self, connections, T, nodes):
        # check attribute in_service of all lines
        for i in self.lines.values():
            if i.in_service == 0:
                broken_line = i.label
                # check presence of broken line in connections
                for j in connections:
                    if broken_line in j.path:
                        # update traffic matrix
                        r = 0
                        c = 0
                        for k in nodes:
                            if j.input == k:
                                break
                            r += 1
                        for k in nodes:
                            if j.output == k:
                                break
                            c += 1
                        T[r][c] += j.bit_rate

                        # update connection
                        j.path = 'Path failure'
                        j.bit_rate = 0
                        j.latency = None
                        j.snr = 0

        # add new connections to saturate the traffic matrix
        connections = self.manage_traffic(T, nodes, connections)

        return connections

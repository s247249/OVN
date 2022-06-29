import pandas as pd


class Network7:
    def update_logger(self, epoch_time, path, channel_ID, bit_rate):
        row_dict = {'Epoch Time': epoch_time, 'Path': path, 'Channel ID': channel_ID, 'Bit Rate': bit_rate}
        logger_row = pd.DataFrame(row_dict, index=[0])
        self._logger.append(logger_row)

    def strong_failure(self, label):
        self.lines[label].in_service = 0

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

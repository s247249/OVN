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
    def traffic_recovery(self):
        return

class Network7:
    # 2. Add a new method to the class Network called update logger() that just
    #    add a series with the mentioned labels to the logger with the information
    #    related to the current allocated connection. The update of the logger is
    #    performed immediately after the update of the routing-space.
    def update_logger(self, epoch_time, path, channel_ID, bit_rate):
        self.logger['Epoch Time'].add(epoch_time)
        self.logger['Path'].add(path)
        self.logger['Channel ID'].add(channel_ID)
        self.logger['Bit Rate'].add(bit_rate)
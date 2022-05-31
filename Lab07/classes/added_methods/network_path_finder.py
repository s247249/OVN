class PathFind():
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

    def find_best_snr(self, in_node, out_node):
        best_snr = 0
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
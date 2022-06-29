import math
import pandas as pd


from ..signal_information import Lightpath


class PathFind():
    def weighted_paths_gen(self, sig_pow=0.001):
        path_dict = {}
        pandas_dict = {'Routes': list(),
                       'Path': list(),
                       'signal_power': list(),
                       'noise_power': list(),
                       'latency': list(),
                       'SNR': list()
                       }

        # generate strings for 'Path' and 'Routes' of pandas_dict
        nodes = self.nodes.keys()
        for i in nodes:
            for j in nodes:
                if i != j:
                    path_dict[i + "->" + j] = self.find_paths(i, j)

        for i in path_dict.keys():
            for j in path_dict[i]:
                pandas_dict['Routes'].append(i)
                pandas_dict['Path'].append(j)

                signal = Lightpath(sig_pow)
                signal.path = list(str(j))
                spectral_info = self.probe(signal)
                for k in spectral_info.keys():
                    pandas_dict[k].append(spectral_info[k])

                SNR = 10 * math.log(spectral_info['signal_power']/spectral_info['noise_power'], 10)
                pandas_dict['SNR'].append(SNR)

        pandas_dict['Signal_power (W)'] = list(pandas_dict['signal_power'])
        pandas_dict['Noise_power (W)'] = list(pandas_dict['noise_power'])
        pandas_dict['Latency (s)'] = list(pandas_dict['latency'])
        pandas_dict['SNR (dB)'] = list(pandas_dict['SNR'])
        del pandas_dict['signal_power']
        del pandas_dict['noise_power']
        del pandas_dict['latency']
        del pandas_dict['SNR']

        df = pd.DataFrame(pandas_dict)
        return df

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
                path = self.route_space['Path'][cnt]

                # lines.in_service check
                flag = 0
                path_list = list(path)
                for j in range(0, len(path_list) - 1):
                    if self.lines[path_list[j] + path_list[j + 1]].in_service == 0:
                        flag = 1
                        break
                if flag:
                    cnt += 1
                    continue

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
                path = self.weighted_paths['Path'][cnt]

                # lines.in_service check
                flag = 0
                path_list = list(path)
                for j in range(0, len(path_list) - 1):
                    if self.lines[path_list[j] + path_list[j + 1]].in_service == 0:
                        flag = 1
                        break
                if flag:
                    cnt += 1
                    continue

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
from ..connection import Connection


class Network6:
    def manage_traffic(self, T, nodes, connections):
        for i in range(len(T)):
            for j in range(len(T)):
                # I want to stream a single connection at a time
                # in stream, i want to occupy every line of T[i][j] used in the path
                while T[i][j] > 0:
                    connection = Connection(nodes[i], nodes[j])
                    path = self.stream(connection, 'snr')
                    connections.append(connection)
                    if connection.bit_rate == 0:
                        connection.path = 'None'
                        break
                    connection.path = path
                    # occupy bit-rate
                    T[i][j] -= connection.bit_rate
                    if T[i][j] < 0:
                        T[i][j] = 0

        return connections

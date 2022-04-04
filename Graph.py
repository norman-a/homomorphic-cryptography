import random
import numpy as np
import pprint
import networkx as nx
import matplotlib.pyplot as plt


class Graph(object):

    def __init__(self, size):
        self.init_size = size
        self.keys = []
        self.mappings = {}
        self.vertex_list = [x for x in range(0, size)]
        self.edge_list = []


        for i in range(0, size):
            for j in range(i + 1, size):
                weight = np.random.randint(2, 10)
                # o = np.random.randint(0, 2)
                self.edge_list.append((i, j, weight))

        # print(self.edge_list)
        print(self.edge_list)

    def get_edge_list(self):
        return self.edge_list
    def get_keys(self):
        return self.keys
    def get_mappings(self):
        return self.mappings
    def create_edge_list(self, size):
        edges = []
        for i in range(0, size):
            for j in range(i + 1, size):
                edges.append((i, j, np.random.randint(1, 10)))
        #      print ( edges)
        return edges

    def create_adj_matrix(self):
        matrix = np.zeros((len(self.vertex_list), len(self.vertex_list))).astype(str)
        for edge in self.edge_list:
            v1 = edge[0]
            v2 = edge[1]
            weight = edge[2]
            if v1 == v2:
                matrix[v1][v2] = '.'
            else:
                matrix[v1][v2] = weight
                matrix[v2][v1] = weight
            return matrix

    def encrypt_g2(self):
        alpha = np.random.randint(1, 5)
        beta = np.random.randint(1, 5)
        gamma = np.random.randint(1, 5)
        delta = np.random.randint(1, 5)
        n1 = len(self.vertex_list)
        n = alpha * n1 + beta
        n2 = n + n1
        m = int((gamma * n2) * ((n2 - 1)/2) + delta)
        for i in range(n1, n + 1):
            self.vertex_list.append(i)
        j = 0
        while j < m:
            x = random.choice(self.vertex_list)
            y = random.choice(self.vertex_list)
            if x == y:
                j = j - 1
                continue
            weight = np.random.randint(1, 10)
            self.edge_list.append((x, y, weight))
            #   print(self.edge_list)
            o = np.random.randint(0, 2) # 0 signals addition and 1 multiplication
            for key in self.keys:
                if (key[0] == x and key[1] == y) or (key[0] == y and key[1] == x):
                    o = key[3]
                    break
            self.keys.append((x, y, weight, o))
            #  print(self.keys )
            j = j + 1
        self.edge_list = sorted(self.edge_list, key=lambda t: (t[0], t[1]))
        #  print(self.edge_list)
        self.keys = sorted(self.keys, key=lambda t: (t[0], t[1]))
        # print(self.edge_list)

    # #  print(self.edge_list)
    #     print(self.keys_dict)

    def encrypt_g3(self):
        # merge edges
        current_v1 = self.edge_list[0][0]
        current_v2 = self.edge_list[0][1]
        start_weight = 0
        current_op = self.keys[0][3]
        new_edge_list = []
        to_remove = []
        for edge in self.edge_list:
            if not (current_v1 == edge[0] and current_v2 == edge[1]):
                new_edge = (current_v1, current_v2, start_weight)
                new_edge_list.append(new_edge)
                current_v1 = edge[0]
                current_v2 = edge[1]
                start_weight = 0
                for key in self.keys[:-1]:
                    if key[0] == current_v1 and key[1] == current_v2:
                        current_op = key[3]
                        break
            if current_op == 0:
                start_weight = start_weight + edge[2]
            elif current_op == 1:
                if start_weight == 0:
                    start_weight = 1
                start_weight = start_weight * edge[2]
        self.edge_list = new_edge_list
        # merge duplicates
        for i in range(0, len(self.edge_list)):
            for j in range(i + 1, len(self.edge_list)):

                if self.edge_list[i][0] == self.edge_list[j][1] and self.edge_list[i][1] == self.edge_list[j][0]:
                    for key in self.keys[:-1]:
                        if key[0] == self.edge_list[j][0] and key[1] == self.edge_list[j][1]:
                            current_op = key[3]
                    start_weight = self.edge_list[i][2]
                    if current_op == 0:
                        start_weight = start_weight + self.edge_list[j][2]
                    elif current_op == 1:
                        if start_weight == 0:
                            start_weight = 1
                        start_weight = start_weight * self.edge_list[j][2]
                    temp = list(self.edge_list[i])
                    temp[2] = start_weight
                    self.edge_list[i] = tuple(temp)
                    to_remove.append(self.edge_list[j])
        for edge in to_remove:
            self.edge_list.remove(edge)
        self.edge_list = sorted(self.edge_list, key=lambda t: (t[0], t[1]))
        # scramble vertices
        new_vertices = []
        key_pairs = []
        not_unique_generated = True
        for vertex in self.vertex_list:
            while not_unique_generated:
                new_vertex = np.random.randint(len(self.vertex_list) * 10)
                if new_vertex in new_vertices or new_vertex in self.vertex_list:
                    continue
                else:
                    new_vertices.append(new_vertex)
                    self.mappings[vertex] = new_vertex
                    key_pairs.append((vertex, new_vertex))
                    not_unique_generated = False
            not_unique_generated = True
        self.keys.append(key_pairs)
        self.vertex_list = new_vertices
        # update edges

        print(self.keys[-1])
        # print(self.mappings)
        # for i in range(0, len(self.edge_list)):
        #     for mapping in self.keys[-1]:
        #         if self.edge_list[i][0] == mapping[0]:
        #             temp = list(self.edge_list[i])
        #             temp[0] = mapping[1]
        #             self.edge_list[i] = tuple(temp)
        #         if self.edge_list[i][1] == mapping[0]:
        #             temp = list(self.edge_list[i])
        #             temp[1] = mapping[1]
        #             self.edge_list[i] = tuple(temp)
        # self.edge_list = sorted(self.edge_list, key=lambda t: (t[0], t[1]))

        print("keys: \n", self.keys)
        print("G3 edge list:\n", self.edge_list)

    def decrypt(self):
        # restore vertices
        new_vertices = []
        for i in range(0, len(self.edge_list)):
            for mapping in self.keys[-1]:
                if self.edge_list[i][0] == mapping[1]:
                    temp = list(self.edge_list[i])
                    temp[0] = mapping[0]
                    self.edge_list[i] = tuple(temp)
                if self.edge_list[i][1] == mapping[1]:
                    temp = list(self.edge_list[i])
                    temp[1] = mapping[0]
                    self.edge_list[i] = tuple(temp)
        for mapping in self.keys[-1]:
            new_vertices.append(mapping[0])
        self.vertex_list = new_vertices
        self.edge_list = sorted(self.edge_list, key=lambda t: (t[0], t[1]))
        # remove added vertices and their edges
        to_remove_vert = []
        to_remove_edges = []
        for i in range(0, len(self.vertex_list)):
            if i > self.init_size - 1:
                to_remove_vert.append(self.vertex_list[i])
                for j in range(0, len(self.edge_list)):
                    if self.edge_list[j][0] == i:
                        if self.edge_list[j] not in to_remove_edges:
                            to_remove_edges.append(self.edge_list[j])
                    if self.edge_list[j][1] == i:
                        if self.edge_list[j] not in to_remove_edges:
                            to_remove_edges.append(self.edge_list[j])
        for edge in to_remove_edges:
            self.edge_list.remove(edge)
        for vertex in to_remove_vert:
            self.vertex_list.remove(vertex)
        self.edge_list = sorted(self.edge_list, key=lambda t: (t[0], t[1]))
        # recalculate weights
        for i in range(len(self.edge_list)):
            current_weight = self.edge_list[i][2]
            for key in self.keys[:-1]:
                if (self.edge_list[i][0] == key[0] and self.edge_list[i][1] == key[1]) or (self.edge_list[i][0] == key[1] and self.edge_list[i][1] == key[0]):
                    current_op = key[3]
                    if current_op == 0:
                        current_weight = current_weight - key[2]
                    if current_op == 1:
                        if key[2] == 0:
                            continue
                        else:
                            current_weight = current_weight / key[2]
            temp = list(self.edge_list[i])
            temp[2] = int(current_weight)
            self.edge_list[i] = tuple(temp)

    def visualize(self):
        """
        Using networkx and matplt libraries draw the graph
        """
        # create the networkx graph and add the edges to it
        G = nx.Graph()
        for e in self.edge_list:
            G.add_edge(e[0], e[1], weight=e[2])
        # spring_layout will make the graph look cleaner as opposed to
        # random positions for each node.
        pos = nx.spring_layout(G)
        nx.draw(G, pos,with_labels= True, node_color='r')

        # plot weights on the labels
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.axis('off')
        plt.show()

    def visualize_without_labels(self):
        """
        To be used for encrypt_g2, when there are multiple edges between each
        vertex, in which case networkx doesn't allow labeling them
        :return:
        """
        edges = []
        for e in self.edge_list:
            edges.append((e[0], e[1]))
        G = nx.MultiGraph(edges)
        pos = nx.random_layout(G)
        nx.draw_networkx(G, pos, node_color = 'r', with_labels=True)
        ax = plt.gca()
        for e in G.edges:
            ax.annotate("",
                        xy=pos[e[0]], xycoords='data',
                        xytext=pos[e[1]], textcoords='data',
                        arrowprops=dict(arrowstyle="->", color="0.5",
                                        shrinkA=5, shrinkB=5,
                                        patchA=None, patchB=None,
                                        connectionstyle="arc3,rad=rrr".replace('rrr',str(0.3*e[2])),),)
        plt.axis('off')
        plt.show()





    def find_weight(self, v1, v2):
        mapped_v1 = None
        mapped_v2 = None
        for key in self.keys[-1]:
            if v1 == key[0]:
                mapped_v1 = key[1]
            if v2 == key[0]:
                mapped_v2 = key[1]
        for edge in self.edge_list:
            if edge[0] == mapped_v1 and edge[1] == mapped_v2:
                return edge[2]



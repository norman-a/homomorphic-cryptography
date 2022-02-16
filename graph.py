import pprint
from collections import defaultdict
import random


class Graph(object):
    """ Graph data structure, undirected by default. """

    def __init__(self, directed=False):
        self.adj_list = {}
        self.vertex_count = 0
        self.edge_count = 0
        self._directed = directed
        self._key = []

    def return_key(self):
        return self._key

    def in_key(self, v1, v2):
        """
        returns whether there's a list with the first two elements being v1 and
        v2 to be used in encrypt_g2()
        """
        for element in self._key:
            if (element[0] == v1 and element[1] == v2) or \
                    (element[0] == v2 and element[1] == v1):
                return element
        return None

    def add_vertex(self, v):
        if v in self.adj_list:
            print("vertex ", v, " already exists!")
        else:
            self.adj_list[v] = []
            self.vertex_count += 1

    def add_edge(self, v1, v2, w=None):
        if v1 not in self.adj_list:
            print("vertex ", v1, " doesn't exist!")
        elif v2 not in self.adj_list:
            print("vertex ", v2, " doesn't exist!")
        elif v1 == v2:
            print("two vertices can't be equal!")
        #elif [v2, w] in self.adj_list[v1]:
        #    print(v1, ", ", v2, ", ", w, "edge already exists!")
        else:
            if not self._directed:
                temp2 = [v1, w]
                self.adj_list[v2].append(temp2)
            temp1 = [v2, w]
            self.adj_list[v1].append(temp1)
            self.edge_count += 1

    def remove_vertex(self, v):
        if v in self.adj_list:
            for edge in self.adj_list[v]:
                self.remove_edge(v, edge[0], edge[1])
            self.adj_list.pop(v)

    def remove_edge(self, v1, v2, w=None):
        if v1 in self.adj_list and v2 in self.adj_list:
            self.adj_list[v1].remove([v2, w])
            if [v1, w] in self.adj_list[v2]:
                self.adj_list[v2].remove([v1, w])
            return True
        else:
            return False

    def encrypt_g2(self):
        """
        Encryption of the graph by adding sufficient vertices n and sufficient edges m
        to the graph
        """
        alpha = random.randint(1, 10)
        beta = random.randint(1, 10)
        gamma = random.randint(1, 10)
        delta = random.randint(1, 10)
        n_1 = len(self.adj_list.keys())
        n = alpha * n_1 + beta
        n_2 = n + n_1
        m = int((gamma * n_2) * ((n_2 - 1)/2) + delta)

        # add vertices to the graph
        for i in range(1, n + 1):
            x = n_1 + i
            self.add_vertex(x)

        self._key.append(n_1)
        # add edges to the graph
        k = 0
        while k < m:
            x = random.choice(list(self.adj_list.keys()))
            y = random.choice(list(self.adj_list.keys()))
            if x == y:
                k -= 1
                continue
            w = random.randint(1, 10)
            self.add_edge(x, y, w)
            o = random.randint(0, 1)
            self._key.append([x, y, w, o])
            k += 1
        # sort the key to be able to merge edges in encrypt_g3()
        # self._key.sort()
        print(self._key)

    def encrypt_g3(self):
        """
        further encryption of the graph, by collapsing all the edges between
        each pair of vertices in the graph into one by adding/multiplying their
        weights.
        """
        # get the first item of the ._key and set it to current
        curr_v1, curr_v2, curr_w = self._key[1][0], self._key[1][1], self._key[1][2]

        # starting from the second item, iterate through the edges
        for edge in self._key[2:]:
            # remove every edge and calculate the weight associated between the
            # current pair
            self.remove_edge(edge[0], edge[1], edge[2])
            if edge[0] == curr_v1 and edge[1] == curr_v2:
                if edge[3] == 0:
                    curr_w += edge[2]
                else:
                    curr_w *= edge[2]

            else:
                # add the final edge and set current to the next pair
                self.add_edge(curr_v1, curr_v2, curr_w)
                curr_v1 = edge[0]
                curr_v2 = edge[1]
                curr_w = edge[2]
        self.add_edge(curr_v1, curr_v2, curr_w)
        random_vert_list = []
        key_mapping = []
        for _ in range(self.vertex_count * 2):
            r = random.randint(1, 1000)
            if r not in random_vert_list:
                random_vert_list.append(r)
        new_adj_list = {}
        for v in self.adj_list:
            i = random.randint(0, len(random_vert_list) - 1)
            new_v = random_vert_list[i]
            random_vert_list.remove(new_v)
            new_adj_list[new_v] = self.adj_list[v]
            # vertex mappings are a tuple that represents hidden vertex -> original vertex as (hidden, original)
            key_mapping.append((new_v, v))
        for v in new_adj_list:
            edges = new_adj_list[v]
            for i in range(len(edges) - 1):
                for pair in key_mapping:
                    if edges[i][0] == pair[1]:
                        edges[i][0] = pair[0]
            new_adj_list[v] = edges
        self._key.append(key_mapping)
        self.adj_list = new_adj_list

    def decrypt(self):
        # first we restore vertices to their original identities
        new_adj_list = {}
        for v in self.adj_list:
            for pair in self._key[-1]:
                if v == pair[0]:
                    new_adj_list[pair[1]] = self.adj_list[v]
        for v in new_adj_list:
            edges = new_adj_list[v]
            for i in range(len(edges) - 1):
                for pair in self._key[-1]:
                    if edges[i][0] == pair[0]:
                        edges[i][0] = pair[1]
            new_adj_list[v] = edges
        self.adj_list = new_adj_list
        iterate = self.adj_list.copy()
        for v in iterate:
            if v > self._key[0]:
                self.remove_vertex(v)
        print(self.adj_list)
        for v in self.adj_list:
            i = 0
            for edge in iterate[v]:
                if edge[0] > self._key[0]:
                    del self.adj_list[v][i]
                i += 1
        print(self.adj_list)
        for key in self._key[1:-1]:
            for v in self.adj_list:
                if key[0] == v or key[1] == v:
                    i = 0
                    for edge in self.adj_list[v]:
                        if edge[0] == key[0] or edge[0] == key[1]:
                            if key[3] == 0:
                                self.adj_list[v][i] = [self.adj_list[v][i][0], self.adj_list[v][i][1] - key[2]]
                            else:
                                self.adj_list[v][i] = [self.adj_list[v][i][0], int(self.adj_list[v][i][1]/key[2])]
                        i += 1

    def __str__(self):
        """
        prints all the edges in the graph
        """
        final = ""
        for vertex in self.adj_list:
            for edge in self.adj_list[vertex]:
                final += "{} -> {}, edge weight: {} \n".format(vertex,
                                                               edge[0], edge[1])
        return final

"""
    def remove_edge(self, v1, v2, w=None):
        if v1 in self.adj_list and v2 in self.adj_list \
                and [v2, w] in self.adj_list[v1] and [v1, w] in self.adj_list[v2]:
            self.adj_list[v1].remove([v2, w])
            if not self._directed:
                self.adj_list[v2].remove([v1, w])
            return True
        else:
            return False
"""
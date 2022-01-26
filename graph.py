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
        elif [v2, w] in self.adj_list[v1]:
            print(v1, ", ", v2, ", ", w, "edge already exists!")
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
        if v1 in self.adj_list and v2 in self.adj_list \
           and [v2, w] in self.adj_list[v1] and [v1, w] in self.adj_list[v2]:
            self.adj_list[v1].remove([v2, w])
            if not self._directed:
                self.adj_list[v2].remove([v1, w])
            return True
        else:
            print("Edge doesn't exist!")
            return False

    def encrypt_g2(self):
        """
        Encryption of the graph by adding 20 random vertices and 50 random edges
        to the graph
        """
        # add 20 vertices to the graph
        for _ in range(20):
            x = random.randint(0, 50)
            self.add_vertex(x)

        # add 50 edges to the graph
        for _ in range(50):
            x = random.choice(list(self.adj_list.keys()))
            y = random.choice(list(self.adj_list.keys()))
            if x == y:
                continue
            w = random.randint(1, 10)
            self.add_edge(x, y, w)
            if self.in_key(x, y):
                self._key.append([x, y, w, self.in_key(x, y)[3]])
            else:
                o = random.randint(0, 1)
                self._key.append([x, y, w, o])

        # sort the key to be able to merge edges in encrypt_g3()
        self._key.sort()

    def encrypt_g3(self):
        """
        further encryption of the graph, by collapsing all the edges between
        each pair of vertices in the graph into one by adding/multiplying their
        weights.
        """
        # get the first item of the ._key and set it to current
        curr_v1, curr_v2, curr_w = self._key[0][0], self._key[0][1], self._key[0][2]

        # starting from the second item, iterate through the edges
        for edge in self._key[1:]:
            # remove every edge and calculate the weight associated between the
            # current pair
            self.remove_edge(edge[0], edge[1], edge[2])
            if edge[0] == curr_v1 and edge[1] == curr_v2:

                if edge[3] == 0:
                    curr_w += edge[2]
                else:
                    curr_w *= edge[2]

            else:
                # add the final egdge and set current to the next pair
                self.add_edge(curr_v1, curr_v2, curr_w)
                curr_v1 = edge[0]
                curr_v2 = edge[1]
                curr_w = edge[2]
        self.add_edge(curr_v1, curr_v2, curr_w)

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


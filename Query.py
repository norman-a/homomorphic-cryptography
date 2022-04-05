class Query:
    # def __init__(self, graph):
    #     self.graph = graph
    #     self.keys = graph.get_keys()
    #     self.map = graph.get_mappings()

    def getEncryptedWeight(self, graph, v1, v2):
        """
        what is the weight of the edge (v1,v2)
        :param graph:
        :param v1:
        :param v2:
        :return:
        """
        count = 0

        mappedv1 = self.retrieveVertice(graph, v1)
        mappedv2 = self.retrieveVertice(graph, v2)
        edge_list = graph.get_edge_list()
        for edge in edge_list:
            if (mappedv1  == edge[0] and mappedv2 == edge[1]) or \
                    (mappedv1  == edge[1] and mappedv2 == edge[0]):
                return edge[2]
        return 0

    def getWeight(self, graph, v1, v2):
        keys = graph.get_keys()
        encrypted_weight = self.getEncryptedWeight(graph,v1, v2)
        for key in keys:
            if (key[0] == v1 and key[1] == v2) or (key[0] == v2 and key[1] == v1):
                if key[3] == 1: encrypted_weight /= key[2]
                else: encrypted_weight -= key[2]
        real_weight = encrypted_weight
        if real_weight < 2:
            print("this edge doesn't exist!")
            return 0
        else:
            return real_weight

    def getPathWeight(self, graph, list_of_vertices):
        total_weight = 0
        for i in range(len(list_of_vertices)-1):
            total_weight += self.getWeight(graph, list_of_vertices[i],
                                           list_of_vertices[i+1])
        return total_weight

    def getHamiltonianWeight(self, graph, list_of_vertices):

        totalWeight = self.getPathWeight(graph, list_of_vertices)
        totalWeight += self.getWeight(graph, list_of_vertices[-1], list_of_vertices[0])
        return totalWeight

    def retrieveVertice(self,graph, vertice):

        keys = graph.get_keys()
        for mapping in keys[-1]:
            if vertice == mapping[0]:
                return mapping[1]
        return 0


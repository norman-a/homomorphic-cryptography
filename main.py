# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from Graph import Graph
from Query import Query
if __name__ == '__main__':
    # start a Query class
    q = Query()

    # initialize a complete graph of 5 nodes
    g = Graph(5)
    g.visualize()

    # first stage of encryption
    g.encrypt_g2()
    # g.visualize()
    g.visualize_without_labels()
    # second stage of encryption
    g.encrypt_g3()
    g.visualize()

    # run the Queries on the encrypted graph
    print(q.getWeight(g, 1, 2)) # returns the hidden weight of an edge
    # returns the total weight of the path of edges between the vertices in
    # the given list
    print(q.getPathWeight(g, [0, 1, 2, 3]))

    # returns the total weight of the edges of the hamiltonian cycle of the
    # given list
    print(q.getHamiltonianWeight(g, [0, 1, 2, 3]))

    # decrypts the graph
    g.decrypt()
    g.visualize()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# This is a sample Python script.
import pprint

from graph import Graph

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    g = Graph()

    g.add_vertex(1)
    g.add_vertex(2)
    g.add_vertex(3)
    g.add_vertex(4)
    g.add_vertex(5)

    g.add_edge(1, 2, 4)
    g.add_edge(1, 3, 7)
    g.add_edge(1, 4, 9)
    g.add_edge(1, 5, 4)
    g.add_edge(2, 3, 5)
    g.add_edge(2, 4, 6)
    g.add_edge(2, 5, 8)
    g.add_edge(3, 4, 10)
    g.add_edge(3, 5, 2)
    g.add_edge(4, 5, 1)
    print(g)

    g.encrypt_g2()
    print(g)

    g.encrypt_g3()
    print(g)

    g.decrypt()
    print(g)
    print(g.adj_list)
# Add the edges between the vertices by specifying
# the from and to vertex along with the edge weights.


# This is a sample Python script.
import pprint

from graph import Graph

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    g = Graph()

    # g.add_vertex(1)
    # g.add_vertex(2)
    # g.add_vertex(3)
    # g.add_vertex(4)
    #
    # g.add_edge(1, 3, 4)
    # g.add_edge(2, 3, 5)
    # g.add_edge(4, 3, 2)
    # print(g)

    g.encrypt_g2()
    print(g)
    print(g.return_key())

    g.encrypt_g3()
    print(g)
# Add the edges between the vertices by specifying
# the from and to vertex along with the edge weights.


    # g.encrypt_g2()
    #
    # print(g.return_key())
    #
    # print(g)
    #
    # g.encrypt_g3()
    # print("--- G3 ----")
    # print(g)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

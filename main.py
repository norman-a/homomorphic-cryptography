from Graph import Graph


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    g = Graph(6)
    g.visualize()

    g.remove_vertex(0)
    g.remove_edge(1, 3)
    g.visualize()

    g.add_edge(2, 5, 3)
    g.add_edge(2, 5, 4)
    g.add_edge(2, 5, 6)
    g.visualize()

    g.encrypt_g2()
    g.visualize()



    g.decrypt()
    g.visualize()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

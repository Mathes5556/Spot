import unittest

from random import randrange
from GPS import dijkstra
from itertools import product
import numpy as np
import random


class DijkstraTest(unittest.TestCase):

    def lattice_graph(self, width, height):
        def graph(vertex):
            x, y = vertex

            susedia = ()

            if x > 0:
                susedia.append((x-1, y), 1)
            if x < width:
                susedia.append((x+1, y), 1)
            if y > 0:
                susedia.append((x, y-1), 2)
            if y < height:
                susedia.append((x, y+1), 2)

            return susedia


            #TODO: definovat graf - mriezku o rozmeroch width x height. vertikalne ciarky su dlhe 2,
            #horiznotalne 1
        return graph

    def random_graph(self, n):
        @memo
        def graph(x):
            return [(i, 1) for i in range(n) if random.random()<0.2]
        return graph

    def setUp(self):
        pass
    


    def test_fixed_graph(self):
        #TODO?: nadefinovat fixny graf a skusit, ci dijkstra funguje
        pass

    def test_not_connected(self):
        #TODO: skusit, ci sa to sprava dobre, ak sa neda najst cesta do cieloveho bodu. skusit sa to
        #da napriklad na lattice_graphe
        pass
    def test_lattice(self):
        n=20
        graph=self.lattice_graph(n,n)
        for i in range(100):
            start=(randrange(n), randrange(n))
            end=(randrange(n), randrange(n))
            dist, _ = dijkstra(graph, start, end)
            self.assertEqual(dist, abs(start[0]-end[0])+2*abs(start[1]-end[1]))

    def test_random_graph(self):
        n=100
        graph=self.random_graph(n)
        vertices=random.sample(list(product(range(n), range(n))),1000)
        mean_distance=np.mean([dijkstra(graph, i, j)[0] for i,j in vertices]) 
        self.assertGreater(mean_distance,1.5)
        self.assertLess(mean_distance,2.5)

class ParsingTest(unittest.TestCase):
    #TODO?: overit, ci nam to uplne jednoduche xml s 5 nodmi (1,2,3,4,5) a 2 cestami (1-3-5, 2-3-4) sparsuje spravne
    pass
unittest.main()   
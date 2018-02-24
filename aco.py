"""Ant Colony Optimization"""
from ant import Ant
from graph import Graph
# import matplotlib.pyplot as plt
import sys

class ACO:
    def __init__(self, graph, params=dict(), algorithm='AS'):
        self.graph = graph
        self.params = params
        self.algorithm = algorithm

        self.num_ants = params.get('num_ants', int(0.8 * graph.num_nodes))
        self.iterations = params.get('iterations', 100)

        self.best_tour_path = []
        self.best_tour_length = sys.maxsize

        # self.to_plot = []

    def iterate(self):
        current_best_tour_path = []
        current_best_tour_length = sys.maxsize

        if self.algorithm == 'ACS' :
            self.params['use_q0'] = True
            self.params['use_local_update'] = True

        self.ants = [Ant(self.graph, params=self.params) for i in range(self.num_ants)]
        for ant in self.ants:
            ant.construct_solution()
            if ant.tour_length < current_best_tour_length:
                current_best_tour_path = ant.tour_path
                current_best_tour_length = ant.tour_length

        if self.best_tour_length > current_best_tour_length:
            self.best_tour_length = current_best_tour_length
            self.best_tour_path = current_best_tour_path

        # self.to_plot.append(current_best_tour_length)
        # print(current_best_tour_length)

    def update_pheromone_as(self):
        # global evaporation
        rho = self.params.get('rho', 0.1)
        for i in range(self.graph.num_nodes):
            for j in range(self.graph.num_nodes):
                old_tao = self.graph.tao(i, j)
                new_tao = (1 - rho) * old_tao
                self.graph.update_tao(i, j, new_tao)
        
        # ants deposition
        Q = self.params.get('Q', 100)
        for ant in self.ants:
            path = ant.tour_path
            length = ant.tour_length
            for i in range(len(path) - 1):
                delta_tao = Q / length
                old_tao = self.graph.tao(path[i], path[i + 1])
                new_tao = old_tao + delta_tao
                self.graph.update_tao(path[i], path[i + 1], new_tao)

    def update_pheromone_mmas(self):
        # global evaporation
        rho = self.params.get('rho', 0.1)
        for i in range(self.graph.num_nodes):
            for j in range(self.graph.num_nodes):
                old_tao = self.graph.tao(i, j)
                new_tao = (1 - rho) * old_tao
                self.graph.update_tao(i, j, new_tao)
        
        # ants deposition
        for ant in self.ants:
            path = ant.tour_path
            length = ant.tour_length
            for i in range(len(path) - 1):
                delta_tao = 1 / length
                old_tao = self.graph.tao(path[i], path[i + 1])
                new_tao = old_tao + delta_tao
                self.graph.update_tao(path[i], path[i + 1], new_tao)

    def update_pheromone_acs(self):
        path = self.best_tour_path
        length = self.best_tour_length
        rho = self.params.get('rho', 0.1)

        for i in range(len(path) - 1):
            delta_tao = 1 / length
            old_tao = self.graph.tao(path[i], path[i + 1])
            new_tao = (1 - rho) * old_tao + rho * delta_tao
            self.graph.update_tao(path[i], path[i + 1], new_tao)
    
    def update_pheromone(self):
        if self.algorithm == 'AS':
            self.update_pheromone_as()
        elif self.algorithm == 'MMAS':
            self.update_pheromone_mmas()
        elif self.algorithm == 'ACS':
            self.update_pheromone_acs()

    def solve(self):
        for i in range(self.iterations):
            self.iterate()
            self.update_pheromone()

        print('===========Result============')
        print(self.best_tour_path)
        print(self.best_tour_length)


if __name__ == '__main__':
    graph = Graph('./data/eil51.tsp')
    as_params = {'iterations': 100, 'alpha': 1, 'beta': 5, 'Q': 100, 'rho': 0.1}
    as_solver = ACO(graph, params=as_params, algorithm='AS')
    as_solver.solve()

    graph.init_tao()
    mmas_params = {'iterations': 100, 'alpha': 1, 'beta': 5, 'rho': 0.1}
    mmas_solver = ACO(graph, params=mmas_params, algorithm='MMAS')
    mmas_solver.solve()

    graph.init_tao()
    acs_params = {'iterations': 100, 'alpha': 1, 'beta': 5, 'rho': 0.1, 'q0': 0.5, 'phi': 0.1}
    acs_solver = ACO(graph, params=acs_params, algorithm='ACS')
    acs_solver.solve()
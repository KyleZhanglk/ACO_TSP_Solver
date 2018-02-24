"""Graph for ACO"""
from edge import Edge
from load_data import load_data


class Graph:
    def __init__(self, filename):
        dist_mat = load_data(filename)
        self.num_nodes = len(dist_mat)
        self.graph = []

        for i in range(self.num_nodes):
            self.graph.append([Edge() for i in range(self.num_nodes)])
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                self.graph[i][j].dist = dist_mat[i][j]
        self.init_tao()

    def dist(self, r, c):
        return self.graph[r][c].dist

    def tao(self, r, c):
        return self.graph[r][c].tao

    def eta(self, r, c):
        # may raise ZeroDivisionError
        return 1 / self.graph[r][c].dist

    def update_tao(self, r, c, value):
        self.graph[r][c].tao = value

    def average_dist(self):
        dist_sum = 0.0
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                dist_sum += self.graph[i][j].dist
        return dist_sum / (self.num_nodes * self.num_nodes)

    def init_tao(self):
        self.tao0 = 1.0 / (self.num_nodes * 0.5 * self.average_dist())
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                self.graph[i][j].tao = self.tao0
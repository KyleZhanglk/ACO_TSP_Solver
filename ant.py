"""Ant for ACO"""
import math
import random

from graph import Graph


class Ant:
    def __init__(self, graph, params=dict()):
        self.graph = graph
        self.start_node = random.randint(0, graph.num_nodes - 1)
        self.visited = [0 for i in range(graph.num_nodes)]
        self.visited[self.start_node] = 1
        self.current_node = self.start_node

        self.tour_path = [self.start_node]
        self.tour_length = 0.0

        self.params = params
        # 'use_q0' means the ant is constructed for ACS algorithm
        self.use_q0 = params.get('use_q0', False)
        self.use_local_update = params.get('use_local_update', False)

    # transition rule for ACS(when q <= q0)
    def transition_rule_1(self):
        beta = self.params.get('beta', 5)
        max_val, next_node = -1, -1
        for i in range(self.graph.num_nodes):
            if self.visited[i]:
                continue
            val = self.graph.tao(self.current_node, i) * math.pow(self.graph.eta(self.current_node, i), beta)
            if val > max_val:
                max_val, next_node = val, i
        return next_node

    # transition rule for AS, MMAS, ACS(when q > q0)
    def transition_rule_2(self):
        alpha = self.params.get('alpha', 1)
        beta = self.params.get('beta', 5)
        sum_prob = 0.0
        select_prob = []
        for i in range(self.graph.num_nodes):
            if self.visited[i]:
                select_prob.append(0.0)
            else:
                select_prob.append(math.pow(self.graph.tao(self.current_node, i), alpha) \
                                * math.pow(self.graph.eta(self.current_node, i), beta))
            sum_prob += select_prob[i]

        prob = random.random() * sum_prob
        next_node = 0
        tmp = select_prob[next_node]
        while self.visited[next_node] or tmp < prob:
            next_node += 1
            if next_node >= self.graph.num_nodes:
                return -1
            tmp += select_prob[next_node]
        
        return next_node

    def next_node(self):
        if not self.use_q0:
            return self.transition_rule_2()

        q0 = self.params.get('q0', 0.5)
        q = random.random()
        if q <= q0:
            return self.transition_rule_1()
        return self.transition_rule_2()

    def construct_solution(self):
        next_node = self.next_node()
        while next_node != -1:
            if self.use_local_update:
                self.local_pheromone_update(next_node)

            self.tour_path.append(next_node)
            self.tour_length += self.graph.dist(self.current_node, next_node)
            self.current_node = next_node
            self.visited[next_node] = 1
            next_node = self.next_node()
        # close the tour
        self.tour_length += self.graph.dist(self.tour_path[-1], self.tour_path[0])

    def local_pheromone_update(self, next_node):
        phi = self.params.get('phi', 0.1)
        val = (1 - phi) * self.graph.tao(self.current_node, next_node) + phi * self.graph.tao0
        self.graph.update_tao(self.current_node, next_node, val)
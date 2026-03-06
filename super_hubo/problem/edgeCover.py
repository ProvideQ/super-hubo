from qubovert import PUBO
from qubovert.problems import Problem

from super_hubo.utils import Graph

class EdgeCover(Problem):
    def __init__(self, graph: Graph):
        self._vertices = graph.V
        self._edges = graph.E
        self._delta = None

    @property
    def E(self):
        return self._edges

    @property
    def V(self):
        return self._vertices
  
    def calc_delta(self):
        self._delta = [[e for e in self._edges if i in e.vertices()] for i in self._vertices]
  
    def to_pubo(self):
        x = [PUBO.create_var("x%d" % i) for i in range(len(self._edges))]
    
        if not self._delta:
            self.calc_delta() 

        H = PUBO()

        for i in self._vertices:
            product = 1
            for j in self._delta[self._vertices.index(i)]:
                product *= (1 - x[self._edges.index(j)])
            H += (1 - product)    

        for i in range(len(self._edges)):
            H -= x[i]

        H.refresh()
        # invert sign of maximization problem for minimizing solver
        return -H

    def convert_solution(self, solution):

        if not isinstance(solution, dict):
            solution = dict(enumerate(solution))

        if not self._delta:
            self.calc_delta()

        included_edges = [int(i[1:]) for i in solution.keys() if solution[i] == 1]

        total_included_vertices = set()
        for included_edge in included_edges:
            total_included_vertices = total_included_vertices.union(self._edges[included_edge].vertices())


        for uncovered_vertex in set(self._vertices).difference(total_included_vertices):
            new_edge = self._delta[self._vertices.index(uncovered_vertex)][0]
            included_edges.append(self._edges.index(new_edge))

        included_set = set(included_edges)

        return {i: (i in included_set) for i in range(len(self._edges))}

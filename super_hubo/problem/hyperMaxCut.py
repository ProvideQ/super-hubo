from qubovert import spin_var, PUSO
from qubovert.problems import Problem
from itertools import combinations

from utils import Vertex, Hypergraph


class HyperMaxCut(Problem):
  def __init__(self, graph: Hypergraph):
    self._vertices = g.V
    self._edges = g.E

  @property
  def E(self):
    return self._edges

  @property
  def V(self):
    return self._vertices


  def to_puso(self):
    n = len(self.E)
    z = [spin_var("z%d" % i) for i in [v.id for v in self.V]]

    if n % 2 == 0:
      m = n
    else:
      m = n - 1

    def c_e(e: list[Vertex]):
      ce = (2 ** (n-2) - 1) / (2 ** (n-2))
      for i in range(2, m + 1, 2):
        s = 0
        for combination in combinations(e, i):
          product = 1
          for factor in combination:
            product *= z[factor.id]
          s += product
        ce -= 1/(2 ** (n - 2)) * s
      return ce


    c = PUSO()
    for e in self.E:
      c += c_e(e)

    return c

  def convert_solution(self, solution, *args, **kwargs):

    if not isinstance(solution, dict):
            solution = dict(enumerate(solution))

    A = set(
        self.V[i] for i, z in solution.items() if z == 1
    )
    B = set(
        self.V[i] for i, z in solution.items() if z != 1
    )

    return A, B
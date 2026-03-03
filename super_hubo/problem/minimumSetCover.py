from qubovert import boolean_var, PUBO
from qubovert.problems import Problem

class MinimumSetCover(Problem):
    def __init__(self, universe: tuple[int], subsets: tuple[tuple[int]]):
        self._universe = universe
        self._subsets = subsets

    @property
    def getUniverse(self):
        return self._universe

    @property
    def getSubsets(self):
        return self._subsets

    def to_pubo(self):
        num_subsets = len(self._subsets)
        num_elements = len(self._universe)

        y = [boolean_var("y%d" % i) for i in range(num_subsets)]
        x = [[self._universe[a] in self._subsets[i] for i in range(num_subsets)] for a in range(num_elements)]

        H = PUBO()

        for a in range(num_elements):
            product = 1
            for i in range(num_subsets):
                product *= (1 - x[a][i] * y[i])
            H += (1 - product)

        for i in range(num_subsets):
            H -= y[i]

        H = -H
        H.set_mapping({f"y{n}": n for n in range(num_subsets)})

        return H

    def convert_solution(self, solution):

        if not isinstance(solution, dict):
                solution = dict(enumerate(solution))

        included_sets = [i for i in solution.keys() if solution[i] == 1]

        total_included_set = set()
        for included_set_index in included_sets:
            total_included_set = total_included_set.union(self._subsets[included_set_index])

        for uncovered_item in set(self._universe).difference(total_included_set):
            if uncovered_item not in total_included_set: # make sure the uncovered item has not been covered in the meantime
                for c_i in [i for i in range(len(self._subsets)) if i not in included_sets]:
                    if uncovered_item in self._subsets[c_i]:
                        included_sets.append(c_i)
                        total_included_set.update(self._subsets[c_i])
                        break

        return {i: (i in included_sets) for i in range(len(self._subsets))}

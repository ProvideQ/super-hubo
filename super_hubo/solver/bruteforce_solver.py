from .solver import Solver
from qubovert import PUBO
from qubovert.utils import solve_pubo_bruteforce

class BruteforceSolver(Solver):
    
    def solve(self, hubo: PUBO):

        solution = solve_pubo_bruteforce(hubo)
        
        obj = solution[0]
        mapped_solution = {}
        bits = solution[1]
        for var in bits:
            mapped_solution[hubo.mapping[var]] = bits[var]
        return mapped_solution, obj

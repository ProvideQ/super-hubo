from .solver import Solver
from qubovert import PUBO
from qubovert.utils import solve_pubo_bruteforce

class BruteforceSolver(Solver):
    
    def solve(self, hubo: PUBO):

        obj, solution = solve_pubo_bruteforce(hubo)
        
        return solution, obj

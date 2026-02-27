from qubovert import PUBO
from typing import Dict, Tuple


class Solver:
    def solve(self, hubo: PUBO) -> Tuple[Dict, int]:
        raise NotImplementedError
from planqk.service.client import PlanqkServiceClient
from .solver import Solver

class KipuSolver(Solver):
    
    SERVICE_ENDPOINT = "https://gateway.hub.kipu-quantum.com/kipu-quantum/miray-advanced-quantum-optimizer---simulator/1.0.0"

    def __init__(self, consumer_key, consumer_secret):
        self._key = consumer_key
        self._secret = consumer_secret


    def solve(self, hubo):
        
        client = PlanqkServiceClient(self.SERVICE_ENDPOINT, self._key, self._secret)

        problem = {}
        for key in hubo.to_enumerated().keys():
            problem[str(key)] = hubo.to_enumerated().get(key)

        request = {
            "problem": problem,
            "problem_type": "binary",
            "shots": 1000,
            "num_interations": 3,
            "num_greedy_passes": 2,
        }

        job = client.run(request=request)

        try:
            job.wait_for_final_state()

            if job.status == "FAILED":
                raise RuntimeError(f"Kipu Solving failed. Kipu execution id: {job.id}.\nrecent logs:\n{job.logs[:3]}")

            result = job.result().result
        except Exception:
            raise RuntimeError("Could not retrieve result from solver.")

        sorted_keys = sorted(result["mapped_solution"].keys(), key=lambda k: int(k))
        sorted_result = {int(key) : result["mapped_solution"][key] for key in sorted_keys} 

        cost = result.get("cost")

        return sorted_result, cost



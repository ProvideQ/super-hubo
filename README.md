# super-hubo

super-hubo is your one-stop solution for handling Higher-Order Unconstrained Binary Optimization (HUBO) problems!

From problem formulation and manipulation using the qubovert library and custom conversions from combinatorial optimization problems through the problem submodule to solving HUBO instances using classical or quantum solvers through our solver submodule, all your HUBO needs are satisfied!

### Installation

super-hubo can be installed using the `%pip install git+https://github.com/ProvideQ/super-hubo.git` command.

### Usage

After installation, combinatorial optimization problem classes can be imported from `super_hubo.problem.{problem name}` and solvers from `super_hubo.solver.{solver name}`.

Currently implemented are HUBO formulation classes for the Minimum Set Cover and Edge Cover problem types, as well as a brute-force classical solver and a solver implementing the Kipu Quantum Miray Solver.

#### Solver Usage

```python
from qubovert import PUBO
from super_hubo.solver.kipu_solver import KipuSolver

x = [PUBO.create_var("x%d" % i) for i in range(4)]

# solver = KipuSolver(consumer_key, consumer_secret)
result, cost = solver. solve(x[0] * x[1]- 2*x[1] +x[1] * x[2] * x[3])

#print(result, cost)
# {'x0': 0, 'x1': 1, 'x2': 0, 'x3': 0} -2
```

Using a solver is straightforward. A solver instance has to be created, passing credentials to the constructor when needed. Then a HUBO problem instance can be passed to the solver's `.solve()` method, this returns the solution mapped as `{name of decision variable: 0 or 1}` and the cost associated to the solution.


### Problem Usage
```python
from super_hubo.problem.edgeCover import EdgeCover
from super_hubo.solver.kipu_solver import KipuSolver
from super_hubo.utils import Vertex, Edge, Graph
from qubovert import PUBO

x = [PUBO.create_var("x%d" % i) for i in range(4)]

C= x[0] * x[1]-2*x[1]+x[1]*x[2] *x[3]
C = PUBO(C)

#solver = KipuSolver("consumer_key", "consumer_secret" )
result = solver.solve(C)
print(result)
# ({'x0': 0, 'x1': 1, 'x2': 0, 'x3': 0}, -2)

v = [Vertex(i) for i in range(5)]
e = [Edge(v[i], v[(i + 1) % 5]) for i in range(5)]

problem = EdgeCover(Graph(v,e))
hubo = problem.to_pubo()
result, cost = solver.solve(hubo)
included_edges = problem.convert_solution(result)

print(hubo.pretty_str())
# x(x0) x(x4) - x(x0) - x(x4) + x(x0) x(x1) - x(x1) + x(x1) x(x2) - x(x2) + x(x2) x(x3) - x(x3) + x(x3) x(x4)
print(included_edges)
# {0: True, 1: True, 2: False, 3: True, 4: False}
```


Using a combinatorial optimization problem is similarly easy. A problem instance is created using the class constructor, which receives the problem statement in its argument. The problem statement format depends on the particular problem type and is documented in the problem definition. 
To convert it to a HUBO, users can call the instance's `.to_pubo()` method, which returns a new qubovert PUBO object. To take the solution of the converted HUBO problem instance and reinterpret it as a solution of the original problem, the original problem instance's `.convert_solution()` method can be used, which takes the HUBO solution as its argument.

### Expanding the toolbox

Expanding the toolbox to add more combinatorial problem types is designed to be as user-friendly as possible.

To add a new combinatorial optimization problem type, users may create a new Python file in the `/problem` subfolder. The new class must inherit qubovert's Problem class.

There must be a custom `__init__` method defined, which takes the problem statement as argument. The format of the problem statement can be freely defined by the creator. The creator may also add auxiliary classes to define these data structures to the `utils.py` file. It must, however, be well-documented in the method documentation. The class should obviously contain variables to store the arguments.

The creator must then define a `.to_pubo()` method, which uses qubovert's `boolean_var` objects to create a qubovert `PUBO` object. This method is responsible for converting the combinatorial optimization problem instance as defined by the problem statement into its equivalent HUBO representation. For combinatorial optimization problems that aim to maximize an objective instead of minimizing it, this method can simply multiply the `PUBO` it returns by \(-1\). It is advisable to use qubovert's 

Finally, the creator should define a `convert_solution()` method, which accepts a HUBO solution in form of a dict mapping decision variable indexes to a boolean value. It then interprets the HUBO solution in the context of the problem the class is describing to provide a valid solution to the original problem. To make sure that one is accessing the expected decision variable, it is advisable to either determine its index using the problem's `.mapping` attribute.


To create a custom solver, a user may create a new Python file in the `/solver` subfolder. The new class must inherit super-hubo's `Solver` class.

If the solver acts as a wrapper around an external solver and needs credentials to access said solver, it should define a custom  `__init__` method. This method should receive the credentials as arguments and store them.

Critically, the solver must define a `.solve()` method, accepting a qubovert `PUBO` instance as argument. In the method body, the HUBO problem gets solved. Its solution must be returned as a pair of objects, the first containing a dict of mapping the names of the decision variables to boolean values describing whether they are included in the solution or not. The information which decision variable name is mapped to which variable index of the PUBO object can be accessed through the problem's `.mapping` property. In a second object, an int containing the cost associated to the solution should be returned.
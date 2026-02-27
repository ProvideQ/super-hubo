class Vertex:
  def __init__(self, id: int):
    self.id = id
  def __repr__(self) -> str:
    return str(self.id)

class Edge:
  def __init__(self, v1: Vertex, v2: Vertex):
    self._vertices = {v1, v2}
  def __repr__(self) -> str:
    return f"{self.v1}->{self.v2}"
  def vertices(self):
    return self._vertices

class Graph:
  def __init__(self, V: tuple[Vertex], E: tuple[Edge]):
    self.V = V
    self.E = E

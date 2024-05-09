from typing import Any, Self

from vetor import Vetor

class Ponto:

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, p2: Self | Vetor) -> Vetor:
        return Vetor(self.x - p2.x, self.y - p2.y, self.z - p2.z)

    def __add__(self, p2: Self | Vetor) -> Self:
        return Ponto(self.x + p2.x, self.y + p2.y, self.z + p2.z)

    def __eq__(self, Outro: Any) -> bool:
        if not isinstance(Outro, Ponto):
            return False
        return self.x == Outro.x and self.y == Outro.y and self.z == Outro.z

    def __mul__(self, n: float) -> Self:
        return Ponto(self.x * n, self.y * n, self.z * n)

    def __rmul__(self, n: float) -> Self:
        return self.__mul__(n)

    def __neg__(self) -> Self:
        return Ponto(-self.x, -self.y, -self.z)
        
    def __repr__(self) -> str:
        return f"Ponto({self.x}, {self.y}, {self.z})"
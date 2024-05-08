from typing import Any, Self

from src.vetor import Vetor

class Ponto:

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, other: Self | Vetor) -> Vetor:
        return Vetor(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other: Self | Vetor) -> Self:
        return Ponto(self.x + other.x, self.y + other.y, self.z + other.z)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Ponto):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __mul__(self, other: float) -> Self:
        return Ponto(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other: float) -> Self:
        return self.__mul__(other)

    def __neg__(self) -> Self:
        return Ponto(-self.x, -self.y, -self.z)
        
    def __repr__(self) -> str:
        return f"Ponto({self.x}, {self.y}, {self.z})"
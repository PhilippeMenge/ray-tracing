from typing_extensions import Any, Self

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

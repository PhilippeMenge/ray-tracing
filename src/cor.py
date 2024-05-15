from typing import Self

from vetor import Vetor

class Cor(Vetor):
    """Classe que representa uma cor RGB e herda de Vetor"""

    def __init__(self, r: float, g: float, b: float):
        super().__init__(min(r, 255), min(g, 255), min(b, 255))

    @property
    def r(self):
        return self.x

    @property
    def g(self):
        return self.y

    @property
    def b(self):
        return self.z



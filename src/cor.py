from vetor import Vetor
from typing_extensions import Self

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

    def __add__(self, outra_cor: Self) -> Self:
        return Cor(
            min(self.r + outra_cor.r, 255),
            min(self.g + outra_cor.g, 255),
            min(self.b + outra_cor.b, 255),
        )



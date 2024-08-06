from abc import ABC, abstractmethod
from vetor import Vetor
from cor import Cor

class Texture(ABC):
    @abstractmethod
    def value(self, u: float, v: float, p: Vetor):
        pass

class SolidTexture(Texture):
    def __init__(self, color: Cor) -> None:
        self.color = color

    def value(self, u: float, v:float, p: Vetor) -> Cor:
        return self.color

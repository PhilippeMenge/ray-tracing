from abc import ABC, abstractmethod
from material import Material
from ray import Ray

class Objeto(ABC):
    def __init__(self, material: Material):
        self.material = material

    @abstractmethod
    def get_intersecao(self, ray: Ray):
        pass

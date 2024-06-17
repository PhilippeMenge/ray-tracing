from triangulo import Triangulo
from ray import Ray
from objeto import Objeto
from material import Material
from vetor import Vetor
from typing_extensions import Self


class MalhaTriangulos(Objeto):

    def __init__(self, material: Material, triangulos: list[Triangulo]):
        super().__init__(material)
        self.triangulos = triangulos

    @property
    def normais(self) -> list[Vetor]:
        normais = []

        for triangulo in self.triangulos:
            normais.append(triangulo.normal)
        return normais

    def get_intersecao(self, ray: Ray) -> tuple[float, Vetor] | tuple[None, None]:
        distancia = float("inf")
        normal = None
        for triangulo in self.triangulos:
            triangulo_dist, triangulo_normal = triangulo.get_intersecao(ray)
            if triangulo_dist is not None and triangulo_dist < distancia:
                distancia = triangulo_dist
                normal = triangulo_normal

        if distancia == float("inf") or normal is None:
            return None, None

        return distancia, normal

    def transform(self, matrix: list[list[float]]) -> Self:
        triangulos = [triangulo.transform(matrix) for triangulo in self.triangulos]
        return self.__class__(self.material, triangulos)

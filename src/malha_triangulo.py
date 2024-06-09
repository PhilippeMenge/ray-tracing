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

    def get_intersecao(self, ray: Ray) -> None | float:
        distancia = float("inf")
        for triangulo in self.triangulos:
            triangulo_dist = triangulo.get_intersecao(ray)
            if triangulo_dist is not None and triangulo_dist < distancia:
                distancia = triangulo_dist

        if distancia is None or distancia == float("inf"):
            return None

        return distancia

    def transform(self, matrix: list[list[float]]) -> Self:
        triangulos = [triangulo.transform(matrix) for triangulo in self.triangulos]
        return self.__class__(self.material, triangulos)

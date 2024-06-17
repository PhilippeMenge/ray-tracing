from vetor import Vetor
from ponto import Ponto
from ray import Ray
from objeto import Objeto
from material import Material
from typing_extensions import Self


class Plano(Objeto):
    """Classe para definir planos 3D e seus métodos."""

    def __init__(self, material: Material, normal: Vetor, ponto: Ponto):
        super().__init__(material)
        self.normal = normal.normalizado()
        self.ponto = ponto

    def get_normal(self) -> Vetor:
        return self.normal

    def get_intersecao(self, ray: Ray) -> tuple[float, Vetor] | tuple[None, None]:
        denominador = ray.direcao.produto_escalar(self.normal)
        numerador = self.normal.produto_escalar(self.ponto - ray.origem)

        if denominador == 0:
            return None, None

        distance = numerador / denominador
        if distance >= 0:
            return distance, self.normal
        else:
            return None, None

    def get_normal_no_ponto(self, ponto: Ponto) -> Vetor:
        return self.normal

    def transform(self, matrix: list[list[float]]) -> Self:
        ponto = self.ponto.transform(matrix)
        normal = self.normal.transform(matrix)
        return self.__class__(self.material, normal, ponto)

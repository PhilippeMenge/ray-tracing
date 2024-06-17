from ponto import Ponto
from vetor import Vetor
from ray import Ray
from objeto import Objeto
from material import Material
import math
from typing_extensions import Self


class Esfera(Objeto):
    """Classe para definir esferas e seus métodos."""

    def __init__(self, material: Material, raio: float, centro: Ponto):
        super().__init__(material)
        self.raio = raio
        self.centro = centro

    def __repr__(self) -> str:
        return f"Sphere(Center:{self.centro}, Radius:{self.raio})"

    def get_intersecao(self, ray: Ray) -> tuple[float, Vetor] | tuple[None, None]:
        oc = ray.origem - self.centro
        a_coeff = ray.direcao.produto_escalar(ray.direcao)
        b_coeff = 2 * ray.direcao.produto_escalar(oc)
        c_coeff = oc.produto_escalar(oc) - self.raio ** 2

        delta = b_coeff**2 - 4 * a_coeff * c_coeff

        EPSILON = 0.0001
        if delta >= 0:
            distancia = (-b_coeff - math.sqrt(delta)) / (2*a_coeff)
            if distancia > EPSILON:
                return distancia, self.get_normal_no_ponto(
                    ray.origem + distancia * ray.direcao
                )
            # O raiz de cima é sempre a menor, logo talvez nem precise desse check abaixo.
            distancia = (-b_coeff + math.sqrt(delta)) / (2*a_coeff)
            if distancia > EPSILON:
                return distancia, self.get_normal_no_ponto(
                    ray.origem + distancia * ray.direcao
                )

        return None, None

    def get_normal_no_ponto(self, ponto: Ponto) -> Vetor:
        return (ponto - self.centro).normalizado()

    def transform(self, matrix: list[list[float]]) -> Self:
        scale_factor = 1
        if matrix[0][0] == matrix[1][1] == matrix[2][2]:
            scale_factor = matrix[0][0]

        centro = self.centro.transform(matrix)
        return self.__class__(self.material, self.raio*scale_factor, centro)


from vetor import Vetor
from ponto import Ponto
from ray import Ray
from objeto import Objeto
from material import Material

class Plano(Objeto):
    """Classe para definir planos 3D e seus métodos."""

    def __init__(self, material: Material, normal: Vetor, ponto: Ponto):
        super().__init__(material)
        self.normal = normal.normalizado()
        self.ponto = ponto

    def get_normal(self) -> Vetor:
        return self.normal

    def get_intersecao(self, ray: Ray) -> float | None:
        denominador = ray.direcao.produto_escalar(self.normal)
        numerador = self.normal.produto_escalar(self.ponto - ray.origem)

        if denominador == 0:
            return None

        distance = numerador / denominador
        if distance >= 0:
            return distance
        else:
            return None

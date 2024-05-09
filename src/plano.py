from vetor import Vetor
from ponto import Ponto
from ray import Ray

class Plano:
    """Classe para definir planos 3D e seus métodos."""

    def __init__(self, normal: Vetor, ponto: Ponto):
        self.normal = normal.normalizado()
        self.ponto = ponto

    def get_normal(self) -> Vetor:
        return self.normal

    def get_intersecao(self, ray: Ray) -> bool:
        if abs(ray.direcao.produto_escalar(self.normal)) == 0:
            return False

        distance = self.normal.produto_escalar(self.ponto - ray.origem) / ray.direcao.produto_escalar(self.normal)
        if distance > 0:
            return True

        return False

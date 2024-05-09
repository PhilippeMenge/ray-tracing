from ponto import Ponto
from ray import Ray

class Esfera:
    """Classe para definir esferas e seus métodos."""

    def __init__(self, raio: float, centro: Ponto):
        self.raio = raio
        self.centro = centro

    def __repr__(self) -> str:
        return f"Sphere(Center:{self.centro}, Radius:{self.raio})"

    def get_intersecao(self, ray: Ray) -> bool:
        oc = ray.get_origem() - self.centro
        a_coeff = ray.direcao.produto_escalar(ray.direcao)
        b_coeff = 2 * ray.direcao.produto_escalar(oc)
        c_coeff = oc.produto_escalar(oc) - self.raio ** 2

        discriminant = b_coeff**2 - 4 * a_coeff * c_coeff

        return discriminant > 0

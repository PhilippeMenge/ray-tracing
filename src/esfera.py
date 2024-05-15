from ponto import Ponto
from ray import Ray
from objeto import Objeto
from material import Material
import math

class Esfera(Objeto):
    """Classe para definir esferas e seus métodos."""

    def __init__(self, material: Material, raio: float, centro: Ponto):
        super().__init__(material)
        self.raio = raio
        self.centro = centro

    def __repr__(self) -> str:
        return f"Sphere(Center:{self.centro}, Radius:{self.raio})"

    def get_intersecao(self, ray: Ray) -> float | None:
        oc = ray.origem - self.centro
        a_coeff = ray.direcao.produto_escalar(ray.direcao)
        b_coeff = 2 * ray.direcao.produto_escalar(oc)
        c_coeff = oc.produto_escalar(oc) - self.raio ** 2

        discriminant = b_coeff**2 - 4 * a_coeff * c_coeff

        if discriminant < 0:
            return None

        distance1 = (-b_coeff + math.sqrt(discriminant)) / (2 * a_coeff)
        distance2 = (-b_coeff - math.sqrt(discriminant)) / (2 * a_coeff)

        return min(distance1, distance2)

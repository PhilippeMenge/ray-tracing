from vetor import Vetor
from ponto import Ponto
from material import Material
from ray import Ray
from objeto import Objeto

class Disco(Objeto):
    """Classe para definir discos e seus métodos."""

    def __init__(self, material: Material, centro: Ponto, raio: float, direcao: Vetor):
        super().__init__(material)
        self.centro = centro
        self.raio = raio
        self.direcao = direcao.normalizado()

    def get_intersecao(self, ray: Ray) -> tuple[float, Vetor] | tuple[None, None]:
        # produto escalar entre a direção normal do disco e a direção do raio 
        denom = self.direcao.produto_escalar(ray.direcao)
        # se for próximo de zero, o raio é paralelo ao plano
        if abs(denom) > 1e-6:
            # distância t ao longo do raio até o ponto de interseção com o plano do disco
            t = (self.centro - ray.origem).produto_escalar(self.direcao) / denom
            if t >= 0:
                ponto_intersecao = ray.origem + ray.direcao * t
                if (ponto_intersecao - self.centro).norma() <= self.raio:
                    return t, self.direcao if denom < 0 else -self.direcao
        return None, None
    
    def get_normal_no_ponto(self, ponto: Ponto) -> Vetor:
        return self.direcao
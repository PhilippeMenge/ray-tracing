from ponto import Ponto
from ray import Ray
from objeto import Objeto
from material import Material

class Triangulo(Objeto):

    def __init__(
            self,
            material: Material,
            arestas: tuple[Ponto, Ponto, Ponto],
    ):
        super().__init__(material)
        self.arestas = arestas

    # Algoritmo de Möller–Trumbore
    def get_intersecao(self, ray: Ray) -> None | float:
        aresta_ab = self.arestas[1] - self.arestas[0]
        aresta_ac = self.arestas[2] - self.arestas[0]

        p = ray.direcao.produto_vetorial(aresta_ac)
        det = aresta_ab.produto_escalar(p)

        EPSILON = 0.0001
        if -EPSILON < det < EPSILON:
            return None

        # Cacular o parametro u. Se u estiver fora do range [0, 1], não há interseção
        inverso_det = 1 / det
        vetor_T = ray.origem - self.arestas[0]
        u = inverso_det * (vetor_T.produto_escalar(p))
        if u < 0 or u > 1:
            return None

        # Cacular o parametro v. Se v estiver fora do range [0, 1], ou u+v>1, não há interseção
        vetor_q = vetor_T.produto_vetorial(aresta_ab)
        v = inverso_det * (ray.direcao.produto_escalar(vetor_q))
        if v < 0 or u + v > 1:
            return None

        # Calcula a distancia da origem até o ponto de interseção
        distance = inverso_det * (aresta_ac.produto_escalar(vetor_q))
        if distance > EPSILON:
            return distance

        return None

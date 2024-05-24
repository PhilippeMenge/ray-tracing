from ponto import Ponto
from ray import Ray
from objeto import Objeto
from material import Material

class Triangulo(Objeto):

    def __init__(
            self,
            material: Material,
            vertices: tuple[Ponto, Ponto, Ponto],
    ):
        super().__init__(material)
        self.vertices = vertices

    """
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
     """

    def get_intersecao(self, ray: Ray) -> None | float:
        aresta_ab = self.vertices[1] - self.vertices[0] # edge1
        aresta_ac = self.vertices[2] - self.vertices[0] # edge2
        aresta_bc = self.vertices[2] - self.vertices[1] # edge3
        
        # Checando interseção com plano o qual o triangulo pertence
        normal = aresta_ab.produto_vetorial(aresta_ac)
        denominador = ray.direcao.produto_escalar(normal)
        numerador = normal.produto_escalar(self.vertices[0] - ray.origem)
        
        # Ray é paralelo ao plano, sem interseção
        if denominador == 0:
            return None

        t = numerador / denominador
        if t < 0:
            return None
        
        area_total = (aresta_ab.produto_vetorial(aresta_ac)).norma() / 2
        ponto_intersecao = ray.origem + t*ray.direcao
        
        area_acp = (((ponto_intersecao - self.vertices[0]).produto_vetorial(aresta_ac)).norma())/2
        u = area_acp/area_total
        
        area_abp = (((ponto_intersecao - self.vertices[0]).produto_vetorial(aresta_ab)).norma())/2
        v = area_abp/area_total

        area_bcp = (((ponto_intersecao - self.vertices[1]).produto_vetorial(aresta_bc)).norma())/2
        w = area_bcp/area_total 
        
        EPSILON = 0.001
        if 1-EPSILON <= (u + w + v) <= 1+EPSILON:
            return t
        
        return None


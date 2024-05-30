from ponto import Ponto
from ray import Ray
from objeto import Objeto
from material import Material
from vetor import Vetor

class Triangulo(Objeto):

    def __init__(
            self,
            material: Material,
            vertices: tuple[Ponto, Ponto, Ponto],
    ):
        super().__init__(material)
        self.vertices = vertices

    @property
    def normal(self) -> Vetor:
        return (self.vertices[1] - self.vertices[0]).produto_vetorial(self.vertices[2] - self.vertices[0])

    def get_intersecao(self, ray: Ray) -> None | float:
        aresta_ab = self.vertices[1] - self.vertices[0] # edge1
        aresta_ac = self.vertices[2] - self.vertices[0] # edge2
        aresta_bc = self.vertices[2] - self.vertices[1] # edge3
        
        # Checando interseção com plano o qual o triangulo pertence
        denominador = ray.direcao.produto_escalar(self.normal)
        numerador = self.normal.produto_escalar(self.vertices[0] - ray.origem)
        
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


from ponto import Ponto
from vetor import Vetor
from ray import Ray
from objeto import Objeto
from material import Material
import math
from typing_extensions import Self
from disco import Disco

class Cilindro(Objeto):
    """Classe para definir cilindros e seus métodos."""

    def __init__(self, material: Material, centro_base: Ponto, altura: float, raio: float, direcao: Vetor):
        super().__init__(material)
        self.centro_base = centro_base  # Centro da base inferior do cilindro
        self.altura = altura  # Altura do cilindro
        self.raio = raio  # Raio das bases do cilindro
        self.direcao = direcao.normalizado()  # Direção normalizada do eixo do cilindro
        self.centro_topo = centro_base + self.direcao * altura  # Centro da base superior do cilindro
        self.base_inferior = Disco(material, self.centro_base, raio, -self.direcao)  # Disco na base inferior do cilindro
        self.base_superior = Disco(material, self.centro_topo, raio, self.direcao)  # Disco na base superior do cilindro

    def get_intersecao(self, ray: Ray) -> tuple[float, Vetor] | tuple[None, None]:
        EPSILON = 0.0001

        # Verifica interseção com a superfície lateral do cilindro
        distancia_cilindro, normal_cilindro = self.get_intersecao_com_cilindro(ray, EPSILON)
        
        # Verifica interseção com a base inferior
        distancia_base_inferior, normal_base_inferior = self.base_inferior.get_intersecao(ray)
        
        # Verifica interseção com a base superior
        distancia_base_superior, normal_base_superior = self.base_superior.get_intersecao(ray)
        
        # Inicializa a interseção mais próxima
        intersecao_mais_proxima = (None, None)

        # Verifica e atualiza a interseção mais próxima
        if distancia_cilindro is not None and distancia_cilindro > EPSILON:
            intersecao_mais_proxima = (distancia_cilindro, normal_cilindro)
        
        if distancia_base_inferior is not None and distancia_base_inferior > EPSILON:
            if intersecao_mais_proxima[0] is None or distancia_base_inferior < intersecao_mais_proxima[0]:
                intersecao_mais_proxima = (distancia_base_inferior, -normal_base_inferior)
        
        if distancia_base_superior is not None and distancia_base_superior > EPSILON:
            if intersecao_mais_proxima[0] is None or distancia_base_superior < intersecao_mais_proxima[0]:
                intersecao_mais_proxima = (distancia_base_superior, -normal_base_superior)

        return intersecao_mais_proxima

    def is_within_height(self, ponto: Ponto) -> bool:
        # Verifica se o ponto está dentro dos limites de altura do cilindro
        projection_height = (ponto - self.centro_base).produto_escalar(self.direcao)
        return 0 <= projection_height <= self.altura

    def get_normal_no_ponto(self, ponto: Ponto) -> Vetor:
        vetor_v = ponto - self.centro_base
        vetor_projecao = self.direcao * vetor_v.produto_escalar(self.direcao)
        vetor_normal = (vetor_v - vetor_projecao).normalizado()
        return vetor_normal

    def get_intersecao_com_cilindro(self, ray: Ray, EPSILON: float) -> tuple[float, Vetor] | tuple[None, None]:
        vetor_origem_base = ray.origem - self.centro_base
        direcao_raio_eixo_cilindro = ray.direcao.produto_escalar(self.direcao)
        origem_base_eixo_cilindro = vetor_origem_base.produto_escalar(self.direcao)
        
        a = 1 - direcao_raio_eixo_cilindro**2
        b = 2 * (ray.direcao.produto_escalar(vetor_origem_base) - direcao_raio_eixo_cilindro * origem_base_eixo_cilindro)
        c = vetor_origem_base.produto_escalar(vetor_origem_base) - origem_base_eixo_cilindro**2 - self.raio**2

        delta = b**2 - 4 * a * c

        # Verifica se 'a' é zero para evitar divisão por zero
        if abs(a) < EPSILON:
            return None, None

        # Verifica interseção com o cilindro em si
        if delta >= 0:
            sqrt_delta = math.sqrt(delta)
            distancia = (-b - sqrt_delta) / (2 * a)
            if distancia > EPSILON:
                ponto_intersecao = ray.origem + distancia * ray.direcao
                if self.is_within_height(ponto_intersecao):
                    return distancia, -self.get_normal_no_ponto(ponto_intersecao)
            distancia = (-b + sqrt_delta) / (2 * a)
            if distancia > EPSILON:
                ponto_intersecao = ray.origem + distancia * ray.direcao
                if self.is_within_height(ponto_intersecao):
                    return distancia, -self.get_normal_no_ponto(ponto_intersecao)

        return None, None

    def transform(self, matrix: list[list[float]]) -> Self:
        centro_base_transformado = self.centro_base.transform(matrix)
        direcao_transformada = self.direcao.transform(matrix).normalizado()
        scale_factor = 1
        if matrix[0][0] == matrix[1][1] == matrix[2][2]:
            scale_factor = matrix[0][0]
        altura_transformada = self.altura * scale_factor
        raio_transformado = self.raio * scale_factor
        return self.__class__(self.material, centro_base_transformado, altura_transformada, raio_transformado, direcao_transformada)
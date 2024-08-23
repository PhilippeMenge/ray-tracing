from ponto import Ponto
from vetor import Vetor
from ray import Ray
from objeto import Objeto
from material import Material
import math
from typing_extensions import Self
from disco import Disco

class Cone(Objeto):
    """Classe para definir cones e seus métodos."""

    def __init__(self, material: Material, vertice: Ponto, altura: float, raio_da_base: float, direcao: Vetor):
        super().__init__(material)
        self.vertice = vertice  # Vértice do cone
        self.altura = altura  # Altura do cone
        self.raio_da_base = raio_da_base  # Raio da base do cone
        self.direcao = direcao.normalizado()  # Direção normalizada do eixo do cone
        self.centro_base = vertice - self.direcao * altura  # Centro da base do cone
        self.hipotenusa = math.sqrt(altura**2 + raio_da_base**2)
        self.cos2 = (altura / self.hipotenusa) ** 2
        self.sin2 = (raio_da_base / self.hipotenusa) ** 2
        self.base = Disco(material, self.centro_base, raio_da_base, self.direcao)  # Disco na base do cone

    def get_intersecao(self, ray: Ray) -> tuple[float, Vetor] | tuple[None, None]:
        EPSILON = 0.0001

        # Verifica interseção com o cone
        distancia_cone, normal_cone = self.get_intersecao_com_cone(ray, EPSILON)
        
        # Verifica interseção com o disco da base
        distancia_disco, normal_disco = self.base.get_intersecao(ray)
        
        # Retorna a interseção mais próxima, se existir
        if distancia_cone is not None and (distancia_disco is None or distancia_cone < distancia_disco):
            return distancia_cone, normal_cone
        
        if distancia_disco is not None and distancia_disco > EPSILON:
            return distancia_disco, normal_disco

        return None, None

    def is_within_height(self, ponto: Ponto) -> bool:
        # Verifica se o ponto está dentro dos limites de altura do cone
        projection_height = -(ponto - self.vertice).produto_escalar(self.direcao)
        return 0 <= projection_height <= self.altura

    def get_normal_no_ponto(self, ponto: Ponto) -> Vetor:
        vetor_v = ponto - self.vertice
        vetor_projecao = self.direcao * vetor_v.produto_escalar(self.direcao)
        vetor_normal = vetor_v - vetor_projecao
        return vetor_normal.normalizado()

    def get_intersecao_com_cone(self, ray: Ray, EPSILON: float) -> tuple[float, Vetor] | tuple[None, None]:
        v = ray.origem - self.vertice
        dv = ray.direcao.produto_escalar(self.direcao)
        vv = v.produto_escalar(self.direcao)

        a = dv**2 - self.cos2
        b = 2 * (dv * vv - ray.direcao.produto_escalar(v) * self.cos2)
        c = vv**2 - v.produto_escalar(v) * self.cos2

        delta = b**2 - 4 * a * c

        # Verifica interseção com o cone em si
        if delta >= 0:
            sqrt_delta = math.sqrt(delta)
            distancia = (-b - sqrt_delta) / (2 * a)
            if distancia > EPSILON:
                ponto_intersecao = ray.origem + distancia * ray.direcao
                if self.is_within_height(ponto_intersecao):
                    return distancia, self.get_normal_no_ponto(ponto_intersecao)
            distancia = (-b + sqrt_delta) / (2 * a)
            if distancia > EPSILON:
                ponto_intersecao = ray.origem + distancia * ray.direcao
                if self.is_within_height(ponto_intersecao):
                    return distancia, self.get_normal_no_ponto(ponto_intersecao)

        return None, None

    def transform(self, matrix: list[list[float]]) -> Self:
        vertice_transformado = self.vertice.transform(matrix)
        direcao_transformada = self.direcao.transform(matrix).normalizado()
        scale_factor = 1
        if matrix[0][0] == matrix[1][1] == matrix[2][2]:
            scale_factor = matrix[0][0]
        altura_transformada = self.altura * scale_factor
        raio_da_base_transformado = self.raio_da_base * scale_factor
        return self.__class__(self.material, vertice_transformado, altura_transformada, raio_da_base_transformado, direcao_transformada)
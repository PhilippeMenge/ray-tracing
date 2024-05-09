from ponto import Ponto
from vetor import Vetor

class Ray:
    """Um raio de luz. Possui um ponto de origem e um vetor que indica sua direção."""

    def __init__(self, origem: Ponto, direcao: Vetor):
        self.origem = origem
        self.direcao = direcao.normalizado()

    def __str__(self) -> str:
        return f"Ray(Origem:{self.origem}, Direcao:{self.direcao.__repr__()})"

    def get_origem(self) -> Ponto:
        return self.origem

    def get_direcao(self) -> Vetor:
        return self.direcao

    def point_at_parameter(self, t: float):
        return self.origem + (self.direcao*t)
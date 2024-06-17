from cor import Cor
from ponto import Ponto
from dataclasses import dataclass


@dataclass
class Luz:
    """Uma fonte de luz na cena"""

    posicao: Ponto
    cor: Cor

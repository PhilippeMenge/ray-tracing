from cor import Cor
from luz import Luz
from vetor import Vetor
from ponto import Ponto
import numpy as np


class Material:
    """Propriedades do material que compõe os objetos"""

    def __init__(
            self,
            cor: Cor,
            coeficiente_difusao: float,
            coeficiente_especular: float,
            coeficiente_ambiental: float,
            coeficiente_rugosidade: float,
    ):
        self.cor = cor
        self.coeficiente_difusao = coeficiente_difusao
        self.coeficiente_especular = coeficiente_especular
        self.coeficiente_ambiental = coeficiente_ambiental
        self.coeficiente_rugosidade = coeficiente_rugosidade

    def get_componente_ambiental(self, cor_ambiente: Cor) -> Cor:
        """Retorna a componente ambiental de acordo com o modelo de Phong."""

        return self.coeficiente_ambiental*cor_ambiente

    def get_componente_difusa(
            self,
            luz: Luz,
            normal_no_ponto: Vetor,
            ponto_intersecao: Ponto
    ) -> Cor:
        """Retorna a componente difusa de acordo com o modelo de Phong."""

        vetor_para_luz = (luz.posicao - ponto_intersecao).normalizado()
        return (
                luz.cor
                * self.cor
                * self.coeficiente_difusao
                * normal_no_ponto.produto_escalar(vetor_para_luz)
        )

    def get_componente_especular(
            self,
            luz: Luz,
            normal_no_ponto: Vetor,
            ponto_intersecao: Ponto,
            posicao_observador: Ponto,
    ) -> Cor:
        """Retorna a componente especular de acordo com o modelo de Phong."""

        vetor_para_luz = (luz.posicao - ponto_intersecao).normalizado()
        vetor_para_luz_refetido = (
                2 * normal_no_ponto
                * (normal_no_ponto.produto_escalar(vetor_para_luz))
                - vetor_para_luz
        )
        vetor_para_observador = (posicao_observador - ponto_intersecao).normalizado()

        return (
                luz.cor
                * self.coeficiente_especular
                * pow(vetor_para_luz_refetido.produto_escalar(vetor_para_observador),
                      self.coeficiente_rugosidade
                      )
        )


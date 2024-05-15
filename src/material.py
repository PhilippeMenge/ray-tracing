from cor import Cor

class Material:
    """Propriedades do material que compõe os objetos (esferas e planos)"""

    def __init__(
            self,
            cor: Cor,
    ):
        self.cor = cor

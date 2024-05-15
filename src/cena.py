from camera import Camera
from cor import Cor
from objeto import Objeto

class Cena:
    """Cena é basicamente um junção de varias coisas, como camera e objetos."""
    def __init__(
            self,
            camera: Camera,
            objetos: list[Objeto],
            cor_ambiente: Cor,
    ):

        self.camera = camera
        self.objetos = objetos
        self.cor_ambiente = cor_ambiente
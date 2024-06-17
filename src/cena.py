from camera import Camera
from cor import Cor
from objeto import Objeto
from luz import Luz


class Cena:
    """Cena é basicamente um junção de varias coisas, como camera e objetos."""
    def __init__(
            self,
            camera: Camera,
            objetos: [Objeto],
            luzes: [Luz],
            cor_ambiente: Cor
    ):
        self.camera = camera
        self.objetos = objetos
        self.luzes = luzes
        self.cor_ambiente = cor_ambiente


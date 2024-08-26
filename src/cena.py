from typing import List
from camera import Camera
from cor import Cor
from objeto import Objeto
from luz import Luz
from luz_retangular import LuzRetangular


class Cena:
    """Cena é basicamente um junção de varias coisas, como camera e objetos."""
    def __init__(
            self,
            camera: Camera,
            objetos: List[Objeto],
            luzes: List[Luz | LuzRetangular],
            cor_ambiente: Cor,
    ):
        self.camera = camera
        self.luzes = luzes
        self.cor_ambiente = cor_ambiente
        self.objetos = objetos


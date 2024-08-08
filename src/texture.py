import math
import numpy as np
from abc import ABC, abstractmethod

from vetor import Vetor
from cor import Cor

class Texture(ABC):
    @abstractmethod
    def value(self, u: float, v: float, p: Vetor):
        pass

class SolidTexture(Texture):
    def __init__(self, color: Cor) -> None:
        self.color = color

    def value(self, u: float, v:float, p: Vetor) -> Cor:
        return self.color
    
class CheckerTexture(Texture):
    def __init__(self, t0, t1):
        self.odd = t0
        self.even = t1

    def value(self, u, v, p):
        sines = math.sin(10 * p.x) * math.sin(10 * p.y) * math.sin(10 * p.z)
        if sines < 0:
            return self.odd.value(u, v, p)
        else:
            return self.even.value(u, v, p)
        
import numpy as np

class ImageTexture(Texture):
    def __init__(self, pixels, width, height):
        self.data = pixels
        self.nx = width
        self.ny = height

    def value(self, u, v, p):
        i = int(u * self.nx)
        j = int((1 - v) * self.ny - 0.001)
        if i < 0:
            i = 0
        if j < 0:
            j = 0
        if i > self.nx - 1:
            i = self.nx - 1
        if j > self.ny - 1:
            j = self.ny - 1
        r = self.data[3 * i + 3 * self.nx * j] / 255
        g = self.data[3 * i + 3 * self.nx * j + 1] / 255
        b = self.data[3 * i + 3 * self.nx * j + 2] / 255
        return Cor(r, g, b)

import math
from typing_extensions import Any, Self

class Vetor:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, v2: Self) -> Self:
        return self.__class__(self.x + v2.x, self.y + v2.y, self.z + v2.z)

    def __sub__(self, v2: Self) -> Self:
        return self.__class__(self.x - v2.x, self.y - v2.y, self.z - v2.z)

    def __mul__(self, v2: float | Self) -> Self:
        if isinstance(v2, Vetor):
            return self.__class__(self.x * v2.x, self.y * v2.y, self.z * v2.z)
        else:
            return self.__class__(self.x * v2, self.y * v2, self.z * v2)

    def __truediv__(self, v2: Any) -> Self:
        if isinstance(v2, Vetor):
            return self.__class__(self.x / v2.x, self.y / v2.y, self.z / v2.z)
        else:
            k = 1.0 / v2
            return self.__class__(self.x * k, self.y * k, self.z * k)

    def __abs__(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalizado(self) -> Self:
        """Retorna o vetor normalizado"""
        return self / abs(self)

    def produto_escalar(self, v2: Self) -> float:
        return self.x * v2.x + self.y * v2.y + self.z * v2.z

    def produto_vetorial(self, v2: Self) -> Self:
        return self.__class__(self.y * v2.z - self.z * v2.y,
                              self.z * v2.x - self.x * v2.z,
                              self.x * v2.y - self.y * v2.x)
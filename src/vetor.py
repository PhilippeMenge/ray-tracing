import math
from typing import Any, Self

class Vetor:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __neg__(self) -> Self:
        return Vetor(-self.x, -self.y, -self.z)
    
    def __eq__(self, v2: Any) -> bool:
        if not isinstance(v2, Vetor):
            return False

        return self.x == v2.x and self.y == v2.y and self.z == v2.z

    def __add__(self, v2: Self) -> Self:
        return self.__class__(self.x + v2.x, self.y + v2.y, self.z + v2.z)

    def __sub__(self, v2: Self) -> Self:
        return self.__class__(self.x - v2.x, self.y - v2.y, self.z - v2.z)

    def __mul__(self, v2: float | Self) -> Self:
        if isinstance(v2, Vetor):
            return self.__class__(self.x * v2.x, self.y * v2.y, self.z * v2.z)
        else:
            return self.__class__(self.x * v2, self.y * v2, self.z * v2)

    def __rmul__(self, v2: float) -> Self:
        return self.__mul__(v2)

    def __truediv__(self, v2: Any) -> Self:
        if isinstance(v2, Vetor):
            return self.__class__(self.x / v2.x, self.y / v2.y, self.z / v2.z)
        else:
            k = 1.0 / v2
            return self.__class__(self.x * k, self.y * k, self.z * k)

    def __abs__(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def norma(self) -> float:
        """Retorna a norma do vetor"""
        return abs(self)

    def normalizado(self) -> Self:
        """Retorna o vetor normalizado"""
        return self / abs(self)

    def __potencia__(self, expoente: int) -> Self:
        return self.__class__(self.x**expoente, self.y**expoente, self.z**expoente)

    def produto_escalar(self, v2: Self) -> float:
        return self.x * v2.x + self.y * v2.y + self.z * v2.z
    
    def produto_vetorial(self, v2: Self) -> Self:
        return self.__class__(self.y * v2.z - self.z * v2.y,
                              self.z * v2.x - self.x * v2.z,
                              self.x * v2.y - self.y * v2.x)
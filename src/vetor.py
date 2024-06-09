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

    def __rmul__(self, other: float) -> Self:
        return self.__mul__(other)

    def __truediv__(self, v2: Any) -> Self:
        if isinstance(v2, Vetor):
            return self.__class__(self.x / v2.x, self.y / v2.y, self.z / v2.z)
        else:
            k = 1.0 / v2
            return self.__class__(self.x * k, self.y * k, self.z * k)

    def __abs__(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __neg__(self) -> Self:
        return self.__class__(-self.x, -self.y, -self.z)

    def norma(self) -> float:
        """Returna a norma do vetor"""
        return abs(self)

    def normalizado(self) -> Self:
        """Retorna o vetor normalizado"""
        return self / abs(self)

    def produto_escalar(self, v2: Self) -> float:
        return self.x * v2.x + self.y * v2.y + self.z * v2.z

    def produto_vetorial(self, v2: Self) -> Self:
        return self.__class__(self.y * v2.z - self.z * v2.y,
                              self.z * v2.x - self.x * v2.z,
                              self.x * v2.y - self.y * v2.x)

    Matrix = list[list[float]]

    def _transform_3x3(self, matrix: Matrix) -> Self:
        """Transforms the vector by a 3x3 matrix"""
        return self.__class__(
            self.x * matrix[0][0] + self.y * matrix[0][1] + self.z * matrix[0][2],
            self.x * matrix[1][0] + self.y * matrix[1][1] + self.z * matrix[1][2],
            self.x * matrix[2][0] + self.y * matrix[2][1] + self.z * matrix[2][2],
            )

    def _transform_4x4(self, matrix: Matrix) -> Self:
        """Transforms the vector by a 4x4 matrix"""
        return self.__class__(
            self.x * matrix[0][0]
            + self.y * matrix[0][1]
            + self.z * matrix[0][2]
            + matrix[0][3],
            self.x * matrix[1][0]
            + self.y * matrix[1][1]
            + self.z * matrix[1][2]
            + matrix[1][3],
            self.x * matrix[2][0]
            + self.y * matrix[2][1]
            + self.z * matrix[2][2]
            + matrix[2][3],
            )

    def transform(self, matrix: Matrix) -> Self:
        if len(matrix) == 3:
            return self._transform_3x3(matrix)

        return self._transform_4x4(matrix)
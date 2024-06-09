from typing_extensions import Any, Self

from vetor import Vetor

class Ponto:

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, p2: Self | Vetor) -> Vetor:
        return Vetor(self.x - p2.x, self.y - p2.y, self.z - p2.z)

    def __add__(self, p2: Self | Vetor) -> Self:
        return Ponto(self.x + p2.x, self.y + p2.y, self.z + p2.z)

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

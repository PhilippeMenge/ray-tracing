from cor import Cor

class Imagem:
    """Classe que representa uma imagen"""

    def __init__(self, Vres: int, Hres: int):
        self.Vres = Vres
        self.Hres = Hres
        self._pixels = [
            [Cor(0, 0, 0) for _ in range(Hres)]
            for _ in range(Vres)
        ]

    def set_pixel(self, x: int, y: int, cor: Cor) -> None:
        """Sobrescreve a cor de um determinado pixel"""
        self._pixels[y][x] = cor

    def gerar_ppm(self, nome_arquivo: str) -> None:
        """Gera um arquivo PPM"""
        with open(nome_arquivo, "w") as f:
            f.write(f"P3 {self.Hres} {self.Vres} 255\n")

            for row in self._pixels:
                for color in row:
                    f.write(f"{color.r} {color.g} {color.b}")
                    f.write("\n")

from ponto import Ponto
from vetor import Vetor
from ray import Ray

class Camera:

    def __init__(self, C: Ponto, M: Ponto, Vup: Vetor, d, Vres, Hres):
        self.C = C
        self.M = M
        self.Vup = Vup
        self.d = d
        self.Vres = Vres
        self.Hres = Hres
        self.vetores_ortonormais()

    def vetores_ortonormais(self):
        self.W = -((self.C - self.M).normalizado())
        self.U = self.Vup.produto_vetorial(self.W).normalizado()
        self.V = self.W.produto_vetorial(self.U).normalizado()

    def novo_local(self, novoC: Ponto):
        self.C = novoC
        self.vetores_ortonormais()

    def nova_mira(self, novoM: Ponto):
        self.M = novoM
        self.vetores_ortonormais()

    def get_ray(self, i: int, j: int) -> Ray:
        """Retorna um ray saindo da camera até o pixel (i, j)"""
        centro_tela = (self.W * self.d) + self.C

        i_normalizado = (i - self.Hres / 2) / self.Hres
        j_normalizado = (j - self.Vres / 2) / self.Vres

        vetor_i_offset = self.U * i_normalizado
        vetor_j_offset = self.V * j_normalizado

        ponto = centro_tela + vetor_i_offset + vetor_j_offset
        direcao = ponto - self.C
        return Ray(self.C, direcao)

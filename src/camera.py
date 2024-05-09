from ponto import Ponto
from vetor import Vetor

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
        self.W = (self.C - self.M).normalizado()
        self.U = self.Vup.produto_vetorial(self.W).normalizado()
        self.V = self.W.produto_vetorial(self.U)

    def novo_local(self, novoC: Ponto):
        self.C = novoC
        self.vetores_ortonormais()

    def nova_mira(self, novoM: Ponto):
        self.M = novoM
        self.vetores_ortonormais()

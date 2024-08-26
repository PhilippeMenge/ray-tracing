from cor import Cor
from vetor import Vetor
from ponto import Ponto
from ray import Ray
from objeto import Objeto
from material import Material

class LuzRetangular(Objeto):
    def __init__(
            self,
            cor: Cor,
            direcao: Vetor,
            posicao: Ponto,
            largura: float,
            altura: float,
    ):
        material_luz = Material(
            cor=cor,
            coeficiente_difusao=0,
            coeficiente_ambiental=0,
            coeficiente_especular=1,
            coeficiente_rugosidade=0,
            coeficiente_reflexao=0,
            coeficiente_refracao=1
        )

        self.cor = cor
        self.direcao = direcao.normalizado()
        self.posicao = posicao
        self.largura = largura
        self.altura = altura
        self.material = material_luz

        # Encontrar dois vetores ortogonais à direção para definir os eixos do retângulo
        if abs(self.direcao.x) > abs(self.direcao.y):
            self.eixo1 = Vetor(-self.direcao.z, 0, self.direcao.x).normalizado() * (largura / 2)
        else:
            self.eixo1 = Vetor(0, self.direcao.z, -self.direcao.y).normalizado() * (largura / 2)
        self.eixo2 = self.direcao.produto_vetorial(self.eixo1).normalizado() * (altura / 2)

    def get_intersecao(self, ray: Ray) -> tuple[float, Vetor] | tuple[None, None]:
        # produto escalar entre a direção normal do retângulo e a direção do raio 
        denom = self.direcao.produto_escalar(ray.direcao)
        # se for próximo de zero, o raio é paralelo ao plano
        if abs(denom) > 1e-6:
            # distância t ao longo do raio até o ponto de interseção com o plano do retângulo
            t = (self.posicao - ray.origem).produto_escalar(self.direcao) / denom
            if t >= 0:
                ponto_intersecao = ray.origem + ray.direcao * t
                # Calcula o vetor da posição do retângulo até o ponto de interseção
                vetor_intersecao = ponto_intersecao - self.posicao
                
                # Projeções do vetor de interseção nos eixos do retângulo
                projecao_largura = vetor_intersecao.produto_escalar(self.eixo1.normalizado())
                projecao_altura = vetor_intersecao.produto_escalar(self.eixo2.normalizado())
                
                # Verifica se o ponto está dentro dos limites do retângulo
                if (
                    -self.largura / 2 <= projecao_largura <= self.largura / 2
                    and -self.altura / 2 <= projecao_altura <= self.altura / 2
                ):
                    return t, self.direcao if denom < 0 else -self.direcao
        return None, None
    
    def get_normal_no_ponto(self, ponto: Ponto) -> Vetor:
        return self.direcao
        


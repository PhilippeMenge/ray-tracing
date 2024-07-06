import numpy as np
from cena import Cena
from ray import Ray
from imagem import Imagem
from camera import Camera
from cor import Cor
from ponto import Ponto
from vetor import Vetor
from esfera import Esfera
from luz import Luz
from objeto import Objeto
from plano import Plano
from material import Material
from triangulo import Triangulo
from malha_triangulo import MalhaTriangulos


def get_intersecao_mais_proxima(
        ray: Ray, cena: Cena
) -> tuple[Ponto, Vetor, Objeto] | tuple[None, None, None]:

    obj_mais_proximo = None
    obj_mais_proximo_dist = float("inf")
    obj_mais_proximo_normal = None
    for obj in cena.objetos:
        dist_intersecao, normal_no_ponto = obj.get_intersecao(ray)
        if (dist_intersecao is not None) and (dist_intersecao < obj_mais_proximo_dist):
            obj_mais_proximo = obj
            obj_mais_proximo_dist = dist_intersecao
            obj_mais_proximo_normal = normal_no_ponto

    if (obj_mais_proximo is None) or (obj_mais_proximo_normal is None):
        return None, None, None

    return (
        ray.origem + ray.direcao*obj_mais_proximo_dist,
        obj_mais_proximo_normal,
        obj_mais_proximo,
    )


def get_cor(
        objeto_intersecao: Objeto,
        ponto_intersecao: Ponto,
        normal_no_ponto: Vetor,
        cena: Cena,
        posicao_observador: Ponto | None = None,
) -> Cor:
    """Retorna a cor de um dado ponto de acordo com o modelo de Phong."""
    posicao_observador = (
        posicao_observador if posicao_observador else cena.camera.C
    )

    # Ambiental
    cor = objeto_intersecao.material.get_componente_ambiental(
        cena.cor_ambiente
    )

    for luz in cena.luzes:

        # Sombra
        raio_luz = Ray(ponto_intersecao, luz.posicao - ponto_intersecao)
        _, _, obj = get_intersecao_mais_proxima(cena=cena, ray=raio_luz)

        if obj is not None and obj != objeto_intersecao:
            continue

        # Difusa
        cor += objeto_intersecao.material.get_componente_difusa(
            luz=luz,
            ponto_intersecao=ponto_intersecao,
            normal_no_ponto=normal_no_ponto,
        )

        # Especular
        cor += objeto_intersecao.material.get_componente_especular(
            luz=luz,
            ponto_intersecao=ponto_intersecao,
            normal_no_ponto=normal_no_ponto,
            posicao_observador=posicao_observador,
        )

    return cor


def get_cor_intersecao(ray: Ray, cena: Cena, level: int = 0) -> Cor:
    """Retorna a colar que deve ser mostrada de acordo com a equação de iluminação de Phong."""
    (
        ponto_intersecao,
        normal_no_ponto,
        objeto_intersecao,
    ) = get_intersecao_mais_proxima(ray, cena)

    if objeto_intersecao is None:
        return cena.cor_ambiente

    cor = cena.cor_ambiente

    cor += get_cor(
        objeto_intersecao=objeto_intersecao,
        ponto_intersecao=ponto_intersecao,
        normal_no_ponto=normal_no_ponto,
        cena=cena,
        posicao_observador=ray.origem,
    )

    max_level = 5
    if level < max_level:
        material = objeto_intersecao.material
        coef_refracao = material.coeficiente_refracao

        # Reflexao
        if material.coeficiente_reflexao > 0:
            direcao_ray_refletido = (
                    -2 * normal_no_ponto
                    * (normal_no_ponto.produto_escalar(ray.direcao))
                    + ray.direcao
            ).normalizado()

            posicao_ray_refletido = ponto_intersecao + (direcao_ray_refletido*0.001)
            ray_refletido = Ray(posicao_ray_refletido, direcao_ray_refletido)
            cor_reflexao = get_cor_intersecao(ray_refletido, cena, level + 1)
            cor += cor_reflexao * material.coeficiente_reflexao

        # Refracao
        if material.coeficiente_refracao > 0:

            """
            Determina se o Ray está saindo ou entrado no objeto.
            Os cálculos de refração assumem as normais para fora do objeto. Quando estamos dentro do objeto, precisamos inverter.
            Ao entrar em um objeto, passamos de n1 (geralmente ar) para n2 (índice do objeto). Ao sair, é o contrário.
            """
            if ray.direcao.produto_escalar(normal_no_ponto) > 0:
                normal_no_ponto = -normal_no_ponto
                coef_refracao = 1 / material.coeficiente_refracao

            cos_i = -normal_no_ponto.produto_escalar(ray.direcao)
            sin2_t = coef_refracao**2 * (1 - cos_i**2)

            #if sin2_t > 1:
            # Total internal reflection

            # Refracao "normal"
            if sin2_t <= 1:
                cos_t = np.sqrt(1 - sin2_t)
                direcao_ray_refratado = (
                        coef_refracao * ray.direcao
                        + (coef_refracao*cos_i - cos_t)
                        * normal_no_ponto
                ).normalizado()

                posicao_ray_refratado = ponto_intersecao + (direcao_ray_refratado*0.001)
                ray_refratado = Ray(posicao_ray_refratado, direcao_ray_refratado)
                cor_refracao = get_cor_intersecao(ray_refratado, cena, level + 1)

                cor += cor_refracao * objeto_intersecao.material.coeficiente_refracao

    return cor


def renderizar_cena(cena: Cena) -> Imagem:
    """Renderiza uma cena e retorna uma imagem PPM."""
    imagem = Imagem(cena.camera.Vres, cena.camera.Hres)

    for y in range(cena.camera.Vres):
        for x in range(cena.camera.Hres):
            ray = cena.camera.get_ray(x, y)
            color = get_cor_intersecao(ray, cena)

            imagem.set_pixel(x, y, color)

    return imagem


def main():

    material_esfera1 = Material(
        cor=Cor(0, 0, 255),
        coeficiente_difusao=0.8,
        coeficiente_ambiental=0.2,
        coeficiente_especular=0.1,
        coeficiente_rugosidade=1,
        coeficiente_reflexao=1,
        coeficiente_refracao=0
    )

    material_esfera2 = Material(
        cor=Cor(0, 255, 0),
        coeficiente_difusao=0.8,
        coeficiente_ambiental=0.2,
        coeficiente_especular=0.1,
        coeficiente_rugosidade=1,
        coeficiente_reflexao=0.1,
        coeficiente_refracao=1
    )

    material_esfera3 = Material(
        cor=Cor(255, 0, 0),
        coeficiente_difusao=0.8,
        coeficiente_ambiental=0.2,
        coeficiente_especular=0.1,
        coeficiente_rugosidade=1,
        coeficiente_reflexao=1,
        coeficiente_refracao=0
    )

    objetos = [
        Esfera(material=material_esfera1, centro=Ponto(-1.25, -1.25, 0), raio=1),
        Esfera(material=material_esfera3, centro=Ponto(-1.25, 1.25, 0), raio=1),
        Esfera(material=material_esfera3, centro=Ponto(1.25, -1.25, 0), raio=1),
        Esfera(material=material_esfera2, centro=Ponto(1.25, 1.25, 0), raio=1),
    ]

    camera = Camera(
        C=Ponto(10, 10, 10),
        M=Ponto(-1.25, -1.25, 0),
        Vup=Vetor(0, 0, -1),
        d=5,
        Vres=500,
        Hres=500
    )

    luzes = [Luz(posicao=Ponto(0, 0, -1), cor=Cor(255, 255, 255))]

    cena = Cena(
        camera=camera,
        objetos=objetos,
        cor_ambiente=Cor(0, 0, 0),
        luzes=luzes
    )

    img = renderizar_cena(cena)
    img.gerar_ppm("test.ppm")


if __name__ == '__main__':
    main()

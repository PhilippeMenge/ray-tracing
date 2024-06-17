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

    # Ambient
    cor = objeto_intersecao.material.get_componente_ambiental(
        cena.cor_ambiente
    )

    for luz in cena.luzes:

        # Diffuse
        cor += objeto_intersecao.material.get_componente_difusa(
            luz=luz,
            ponto_intersecao=ponto_intersecao,
            normal_no_ponto=normal_no_ponto,
        )

        # Specular
        cor += objeto_intersecao.material.get_componente_especular(
            luz=luz,
            ponto_intersecao=ponto_intersecao,
            normal_no_ponto=normal_no_ponto,
            posicao_observador=posicao_observador,
        )

    return cor


def get_cor_intersecao(ray: Ray, cena: Cena) -> Cor:
    """Trace a ray and return the color that should be displayed, according to Phong shading."""
    (
        ponto_intersecao,
        normal_no_ponto,
        objeto_intersecao,
    ) = get_intersecao_mais_proxima(ray, cena)

    if objeto_intersecao is None:
        return cena.cor_ambiente

    cor = Cor(0, 0, 0)

    cor += get_cor(
        objeto_intersecao=objeto_intersecao,
        ponto_intersecao=ponto_intersecao,
        normal_no_ponto=normal_no_ponto,
        cena=cena,
        posicao_observador=ray.origem,
    )

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

    coef_difusao = 0.7
    coef_especular = 0.8
    coef_ambiental = 0.1
    coef_rugosidade = 25

    material_esfera1 = Material(
        cor=Cor(255, 215, 0),
        coeficiente_difusao=coef_difusao,
        coeficiente_ambiental=coef_ambiental,
        coeficiente_especular=coef_especular,
        coeficiente_rugosidade=coef_rugosidade
    )

    material_plano = Material(
        cor=Cor(200, 100, 200),
        coeficiente_difusao=coef_difusao,
        coeficiente_ambiental=coef_ambiental,
        coeficiente_especular=coef_especular,
        coeficiente_rugosidade=coef_rugosidade
    )

    objetos = [
        Esfera(material=material_esfera1, centro=Ponto(0, -2, 0), raio=5),
        Plano(material=material_plano, normal=Vetor(0, 0, 1), ponto=Ponto(0, 0, 0))
    ]

    camera = Camera(
        C=Ponto(100, 0, 1),
        M=Ponto(0, 0, 1),
        Vup=Vetor(0, 0, -1),
        d=5,
        Vres=500,
        Hres=500
    )

    luzes = [Luz(posicao=Ponto(0, -2, 10), cor=Cor(255, 255, 255))]

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

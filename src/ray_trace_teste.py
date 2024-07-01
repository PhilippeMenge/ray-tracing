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

    MAX_DEPTH = 5
    if level < MAX_DEPTH:
        material = objeto_intersecao.material
        normal = normal_no_ponto
        omega = -ray.direcao
        relative_transmission_coeff = material.coeficiente_refracao

        # If the ray is inside the object, the normal should be flipped.
        if normal.produto_escalar(omega) < 0:
            normal = -normal

            # If the ray is inside the object, the transmission coefficient should be inverted.
            relative_transmission_coeff = (
                0
                if relative_transmission_coeff == 0
                else 1 / relative_transmission_coeff
            )

        # Reflection
        if material.coeficiente_reflexao > 0:
            reflected_ray_pos = ponto_intersecao + (normal * 0.01)
            reflected_ray_dir = (
                    2 * normal_no_ponto
                    * (normal_no_ponto.produto_escalar(ray.direcao))
                    - ray.direcao
            ).normalizado()
            reflected_ray = Ray(reflected_ray_pos, reflected_ray_dir)

            cor += (
                    get_cor_intersecao(reflected_ray, cena, level + 1)
                    * material.coeficiente_reflexao
            )

        # Refraction / Transmission
        if material.coeficiente_refracao > 0:
            delta = 1 - (1 / relative_transmission_coeff**2) * (
                    1 - normal.produto_escalar(omega) ** 2
            )

            # If delta is positive, the ray is refracted.
            if delta >= 0:
                inverse_transmission_coeff = 1 / relative_transmission_coeff

                refracted_ray_dir = inverse_transmission_coeff * (
                        ray.direcao - normal.produto_escalar(ray.direcao) * normal
                ) - normal * np.sqrt(delta)
                reflected_ray_pos = ponto_intersecao + (-normal * 0.01)
                refracted_ray = Ray(reflected_ray_pos, refracted_ray_dir)

                cor += (
                        get_cor_intersecao(refracted_ray, cena, level + 1)
                        * material.coeficiente_refracao
                )
            # If delta is negative, the ray is reflected. (Total internal reflection)
            else:
                reflected_ray_dir = (
                        2 * normal_no_ponto
                        * (normal_no_ponto.produto_escalar(ray.direcao))
                        - ray.direcao
                ).normalizado()
                reflected_ray_pos = ponto_intersecao + (normal * 0.01)
                reflected_ray = Ray(reflected_ray_pos, reflected_ray_dir)
                cor += (
                        get_cor_intersecao(reflected_ray, cena, level + 1)
                        * material.coeficiente_refracao
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

    # Vidro
    material_esfera1 = Material(
        cor=Cor(0, 0, 155),
        coeficiente_difusao=0.1,
        coeficiente_ambiental=0.1,
        coeficiente_especular=0.9,
        coeficiente_rugosidade=0,
        coeficiente_reflexao=0.05,
        coeficiente_refracao=1.5
    )

    # Metal
    material_esfera2 = Material(
        cor=Cor(192, 192, 192),
        coeficiente_difusao=0.3,
        coeficiente_ambiental=0.1,
        coeficiente_especular=0.7,
        coeficiente_rugosidade=0.05,
        coeficiente_reflexao=0.8,
        coeficiente_refracao=0
    )

    material_esfera3 = Material(
        cor=Cor(255, 0, 0),
        coeficiente_difusao=0.8,
        coeficiente_ambiental=0.2,
        coeficiente_especular=0.1,
        coeficiente_rugosidade=0.7,
        coeficiente_reflexao=0.05,
        coeficiente_refracao=0
    )

    objetos = [
        Esfera(material=material_esfera2, centro=Ponto(0, 0, 0), raio=2),
        #Esfera(material=material_esfera2, centro=Ponto(-0.5, -3, 1), raio=2),
        #Esfera(material=material_esfera3, centro=Ponto(0.5, 3, 1), raio=2),
        #Plano(material=material_plano, normal=Vetor(0, 0, 1), ponto=Ponto(0, 0, 0))
    ]

    camera = Camera(
        C=Ponto(25, 0, 1),
        M=Ponto(0, 0, 1),
        Vup=Vetor(0, 0, -1),
        d=5,
        Vres=500,
        Hres=500
    )

    luzes = [Luz(posicao=Ponto(0, -10, 10), cor=Cor(255, 255, 255))]

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

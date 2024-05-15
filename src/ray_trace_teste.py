from cena import Cena
from ray import Ray
from imagem import Imagem
from camera import Camera
from cor import Cor
from ponto import Ponto
from vetor import Vetor
from esfera import Esfera
from material import Material


def get_cor_intersecao(ray: Ray, cena: Cena) -> Cor:
    obj_mais_proximo = None
    obj_mais_proximo_dist = float("inf")
    for obj in cena.objetos:
        dist_intersecao = obj.get_intersecao(ray)
        if dist_intersecao is not None:
            if dist_intersecao < obj_mais_proximo_dist:
                obj_mais_proximo = obj
                obj_mais_proximo_dist = dist_intersecao

    if obj_mais_proximo is None:
        return cena.cor_ambiente

    return obj_mais_proximo.material.cor


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
    camera = Camera(
        C=Ponto(0, 0, 0),
        M=Ponto(200, 0, 0),
        Vup=Vetor(0, 1, 0),
        d=90,
        Vres=500,
        Hres=500
    )

    material_esfera = Material(Cor(255, 0, 0))
    objetos = [
        Esfera(material=material_esfera, centro=Ponto(200, 0, 0), raio=1),
    ]

    cena = Cena(
        camera=camera,
        objetos=objetos,
        cor_ambiente=Cor(0, 0, 0),
    )

    img = renderizar_cena(cena)
    img.gerar_ppm("test.ppm")


if __name__ == '__main__':
    main()

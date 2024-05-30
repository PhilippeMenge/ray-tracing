from cena import Cena
from ray import Ray
from imagem import Imagem
from camera import Camera
from cor import Cor
from ponto import Ponto
from vetor import Vetor
from esfera import Esfera
from plano import Plano
from material import Material
from triangulo import Triangulo
from malha_triangulo import MalhaTriangulos


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
    material_esfera1 = Material(Cor(0, 0, 255))
    material_esfera2 = Material(Cor(255, 0, 255))
    material_plano = Material(Cor(0, 255, 255))
    material_triangulo = Material(Cor(0, 0, 255))

    vertices = [
        Ponto(-1, -1, -1),
        Ponto(1, -1, -1),
        Ponto(1, 1, -1),
        Ponto(-1, 1, -1),
        Ponto(-1, -1, 1),
        Ponto(1, -1, 1),
        Ponto(1, 1, 1),
        Ponto(-1, 1, 1),
    ]

    triplas_vertice = [
        (vertices[0], vertices[1], vertices[2]), (vertices[0], vertices[2], vertices[3]),  # Front face
        (vertices[4], vertices[5], vertices[6]), (vertices[4], vertices[6], vertices[7]),  # Back face
        (vertices[0], vertices[3], vertices[7]), (vertices[0], vertices[7], vertices[4]),  # Left face
        (vertices[1], vertices[2], vertices[6]), (vertices[1], vertices[6], vertices[5]),  # Right face
        (vertices[3], vertices[2], vertices[6]), (vertices[3], vertices[6], vertices[7]),  # Top face
        (vertices[0], vertices[1], vertices[5]), (vertices[0], vertices[5], vertices[4])   # Bottom face
    ]

    triangulos = [
        Triangulo(material=material_triangulo, vertices=triplas_vertice[i]) for i in range(len(triplas_vertice))
    ]
    mesh = MalhaTriangulos(material=material_triangulo, triangulos=triangulos)

    objetos = [mesh]

    camera = Camera(
        C=Ponto(10, 0, 0),
        M=Ponto(0, 0, 0),
        Vup=Vetor(0, 0, -1),
        d=5,
        Vres=500,
        Hres=500
    )

    cena = Cena(
        camera=camera,
        objetos=objetos,
        cor_ambiente=Cor(0, 0, 0),
    )

    img = renderizar_cena(cena)
    img.gerar_ppm("test.ppm")


if __name__ == '__main__':
    main()

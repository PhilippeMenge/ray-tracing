import numpy as np

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

    matrix_translacao = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, -1],
        [0, 0, 0, 1]
    ]

    matrix_escala = [
        [4, 0, 0, 0],
        [0, 4, 0, 0],
        [0, 0, 4, 0],
        [0, 0, 0, 1]
    ]

    # Ângulo de rotação em radianos (90 graus)
    theta = np.pi / 2
    rotation_matrix_x = [
        [1, 0, 0, 0],
        [0, np.cos(theta), -np.sin(theta), 0],
        [0, np.sin(theta), np.cos(theta), 0],
        [0, 0, 0, 1]
    ]

    '''
    material_triangulo = Material(Cor(123, 76, 85))
    
    vertices = [
        Ponto(0, 1, 0),
        Ponto(0, -1, 0),
        Ponto(0,  0, 1),
    ]
    
    triplas_vertice = [
        (vertices[0], vertices[1], vertices[2])
    ]
    
    triangulos = [
        Triangle(material=material_triangulo, points=triplas_vertice[t]) for t in range(len(triplas_vertice))
    ]
    
    mesh = TriangleMesh(material=material_triangulo, triangles=triangulos)
    mesh = mesh.transform(rotation_matrix_x)
    '''

    esfera = Esfera(material=material_esfera1, centro=Ponto(0, 0, 0), raio=0.1)
    esfera = esfera.transform(np.dot(matrix_translacao, matrix_escala))

    objetos = [esfera]

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

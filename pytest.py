import unittest
import pygame
from flappybird import Pajaro, ParTubo, frames_to_msec, msec_to_frames, ALTO_VENTANA, ANCHO_VENTANA

class PruebaPajaro(unittest.TestCase):

    def setUp(self):
        pygame.init()
        ala_arriba = pygame.Surface((32, 32))
        ala_abajo = pygame.Surface((32, 32))
        self.pajaro = Pajaro(50, 100, 0, (ala_arriba, ala_abajo))

    def test_posicion_inicial(self):
        self.assertEqual(self.pajaro.x, 50)
        self.assertEqual(self.pajaro.y, 100)

    def test_subir_y_caer(self):
        self.pajaro.milisegundos_para_subir = Pajaro.DURACION_SUBIDA
        y_antes = self.pajaro.y
        self.pajaro.actualizar()
        self.assertLess(self.pajaro.y, y_antes, "El pájaro debe subir")

        self.pajaro.milisegundos_para_subir = 0
        y_antes = self.pajaro.y
        self.pajaro.actualizar()
        self.assertGreater(self.pajaro.y, y_antes, "El pájaro debe caer")

    def test_rectangulo_dimensiones(self):
        rect = self.pajaro.rect
        self.assertEqual(rect.width, Pajaro.ANCHO)
        self.assertEqual(rect.height, Pajaro.ALTO)


class PruebaParTubo(unittest.TestCase):

    def setUp(self):
        pygame.init()
        img_extremo = pygame.Surface((80, 32))
        img_cuerpo = pygame.Surface((80, 32))
        self.tubo = ParTubo(img_extremo, img_cuerpo)

    def test_posicion_inicial(self):
        self.assertEqual(int(self.tubo.x), ANCHO_VENTANA - 1)

    def test_visibilidad(self):
        self.tubo.x = ANCHO_VENTANA / 2
        self.assertTrue(self.tubo.visible)
        self.tubo.x = -ParTubo.ANCHO - 1
        self.assertFalse(self.tubo.visible)

    def test_actualizar_posicion(self):
        x_antes = self.tubo.x
        self.tubo.actualizar()
        self.assertLess(self.tubo.x, x_antes)

    def test_colision(self):
        pajaro = Pajaro(50, 100, 0, (pygame.Surface((32, 32)), pygame.Surface((32, 32))))
        self.tubo.x = pajaro.x
        resultado = self.tubo.colisiona_con(pajaro)
        self.assertIsInstance(resultado, bool)


class PruebaUtilidades(unittest.TestCase):

    def test_frames_a_milisegundos(self):
        self.assertEqual(frames_to_msec(60, fps=60), 1000)

    def test_milisegundos_a_frames(self):
        self.assertEqual(msec_to_frames(1000, fps=60), 60)


if __name__ == '__main__':
    unittest.main()

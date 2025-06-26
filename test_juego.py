import unittest
import pygame
from flappybird import Pajaro, ParTubo, cuadros_a_mseg, mseg_a_cuadros, ALTO_VENTANA, ANCHO_VENTANA


class PruebaPajaro(unittest.TestCase):

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1))  
        ala_arriba = pygame.Surface((32, 32)).convert_alpha()
        ala_abajo = pygame.Surface((32, 32)).convert_alpha()
        ala_arriba.fill((255, 255, 255, 255))
        ala_abajo.fill((255, 255, 255, 255))
        self.pajaro = Pajaro(50, 100, 0, (ala_arriba, ala_abajo))

    def test_posicion_inicial(self):
        self.assertEqual(self.pajaro.x, 50)
        self.assertEqual(self.pajaro.y, 100)

    def test_subir_y_caer(self):
        self.pajaro.mseg_para_subir = Pajaro.DURACION_SUBIDA
        y_antes = self.pajaro.y
        for _ in range(3):
            self.pajaro.actualizar()
        self.assertLess(self.pajaro.y, y_antes, "El pájaro debe subir")

        self.pajaro.mseg_para_subir = Pajaro.DURACION_SUBIDA
        y_antes = self.pajaro.y
        while self.pajaro.mseg_para_subir > 0:
            self.pajaro.actualizar()
        y_cima = self.pajaro.y
        for _ in range(3):
            self.pajaro.actualizar()
        self.assertGreater(self.pajaro.y, y_cima, "El pájaro debe caer")

    def test_rectangulo(self):
        rect = self.pajaro.rect
        self.assertEqual(rect.width, Pajaro.ANCHO)
        self.assertEqual(rect.height, Pajaro.ALTO)

class PruebaParTubo(unittest.TestCase):

    def setUp(self):
        pygame.init()
        img_extremo = pygame.Surface((80, 32)).convert_alpha()
        img_cuerpo = pygame.Surface((80, 32)).convert_alpha()
        img_extremo.fill((255, 255, 255, 255))
        img_cuerpo.fill((255, 255, 255, 255))
        self.tubo = ParTubo(img_extremo, img_cuerpo)

    def test_posicion_inicial(self):
        self.assertAlmostEqual(self.tubo.x, ANCHO_VENTANA - 1, delta=1)

    def test_visibilidad(self):
        self.tubo.x = ANCHO_VENTANA / 2
        self.assertTrue(self.tubo.visible)
        self.tubo.x = -ParTubo.ANCHO - 10
        self.assertFalse(self.tubo.visible)

    def test_actualizar(self):
        x_antes = self.tubo.x
        self.tubo.actualizar()
        self.assertLess(self.tubo.x, x_antes)

    def test_colision(self):
        ala_arriba = pygame.Surface((32, 32)).convert_alpha()
        ala_abajo = pygame.Surface((32, 32)).convert_alpha()
        pajaro = Pajaro(50, 100, 0, (ala_arriba, ala_abajo))
        colision = self.tubo.colisiona_con(pajaro)
        self.assertIsNone(colision, "No debería haber colisión inicialmente")


class PruebaUtilidades(unittest.TestCase):

    def test_frames_a_milisegundos(self):
        self.assertEqual(cuadros_a_mseg(60, fps=60), 1000)

    def test_milisegundos_a_frames(self):
        self.assertEqual(mseg_a_cuadros(1000, fps=60), 60)

if __name__ == '__main__':
    unittest.main()

#ATDD

def test_pajaro_fuera_de_pantalla():
    pajaro = Pajaro(50, ALTO_VENTANA - Pajaro.ALTO / 2, 0,
                    (pygame.Surface((32, 32)), pygame.Surface((32, 32))))
    pajaro.y = ALTO_VENTANA + 1
    assert pajaro.y > ALTO_VENTANA - Pajaro.ALTO

def test_tubo_fuera_de_pantalla():
    tubo = ParTubo(pygame.Surface((80, 32)), pygame.Surface((80, 32)))
    tubo.x = -ParTubo.ANCHO - 1
    assert not tubo.visible

#BDD

def test_scenario_pajaro_sube_y_cae():
    
    #Scenario: Pájaro sube y luego cae
    #Given el pájaro con mseg_para_subir = Pajaro.DURACION_SUBIDA
    #When se llama a actualizar 5 veces
    #Then la posición y del pájaro primero disminuye y luego aumenta
    
    # Given
    ala_up = pygame.Surface((32, 32)).convert_alpha()
    ala_down = pygame.Surface((32, 32)).convert_alpha()
    pajaro = Pajaro(50, 100, Pajaro.DURACION_SUBIDA, (ala_up, ala_down))
    # When
    posiciones = []
    for _ in range(5):
        pajaro.actualizar()
        posiciones.append(pajaro.y)
    # Then
    assert posiciones[0] < 100, "El pájaro debería subir al inicio"
    assert posiciones[-1] > posiciones[2], "El pájaro debería caer después del pico"

def test_scenario_tubo_generacion_y_visibilidad():
    #Scenario: Generación de tubos y visibilidad
    #Given un ParTubo recién creado
    #When se actualiza su posición hasta fuera de la pantalla
    #Then tube.visible pasa de True a False
     
    # Given
    img_ext = pygame.Surface((80, 32)).convert_alpha()
    img_cuerpo = pygame.Surface((80, 32)).convert_alpha()
    tubo = ParTubo(img_ext, img_cuerpo)
    # When
    vis_inicial = tubo.visible
    tubo.x = -ParTubo.ANCHO - 1
    vis_final = tubo.visible
    # Then
    assert vis_inicial is True, "El tubo debe ser visible recién creado"
    assert vis_final is False, "El tubo no debe ser visible una vez fuera de pantalla"
    
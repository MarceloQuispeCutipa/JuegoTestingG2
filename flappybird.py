import math
import os
from random import randint
from collections import deque
import pygame
from pygame.locals import *

FPS = 60
VELOCIDAD_ANIMACION = 0.18
ANCHO_VENTANA = 568
ALTO_VENTANA = 512

class Pajaro(pygame.sprite.Sprite):
    ANCHO = ALTO = 32
    VELOCIDAD_CAIDA = 0.10
    VELOCIDAD_SUBIDA = 0.2
    DURACION_SUBIDA = 333.3

    def __init__(self, x, y, mseg_para_subir, imagenes):
        super(Pajaro, self).__init__()
        self.x, self.y = x, y
        self.mseg_para_subir = mseg_para_subir
        self._img_alas_arriba, self._img_alas_abajo = imagenes
        self._mascara_alas_arriba = pygame.mask.from_surface(self._img_alas_arriba)
        self._mascara_alas_abajo = pygame.mask.from_surface(self._img_alas_abajo)

    def actualizar(self, cuadros_delta=1):
        if self.mseg_para_subir > 0:
            fraccion_subida = 1 - self.mseg_para_subir / Pajaro.DURACION_SUBIDA
            self.y -= (Pajaro.VELOCIDAD_SUBIDA * cuadros_a_mseg(cuadros_delta) *
                       (1 - math.cos(fraccion_subida * math.pi)))
            self.mseg_para_subir -= cuadros_a_mseg(cuadros_delta)
        else:
            self.y += Pajaro.VELOCIDAD_CAIDA * cuadros_a_mseg(cuadros_delta)

    @property
    def imagen(self):
        if pygame.time.get_ticks() % 500 >= 250:
            return self._img_alas_arriba
        else:
            return self._img_alas_abajo

    @property
    def mask(self):
        if pygame.time.get_ticks() % 500 >= 250:
            return self._mascara_alas_arriba
        else:
            return self._mascara_alas_abajo

    @property
    def image(self):
        return self.imagen

    @property
    def rectangulo(self):
        return Rect(self.x, self.y, Pajaro.ANCHO, Pajaro.ALTO)

    @property
    def rect(self):
        return self.rectangulo

class ParTubo(pygame.sprite.Sprite):
    ANCHO = 80
    ALTO_PIEZA = 32
    INTERVALO_AGREGAR = 3000

    def __init__(self, imagen_extremo, imagen_cuerpo):
        super(ParTubo, self).__init__()
        self.x = float(ANCHO_VENTANA - 1)
        self.puntaje_contado = False
        self._imagen = pygame.Surface((ParTubo.ANCHO, ALTO_VENTANA), SRCALPHA)
        self._imagen.convert()
        self._imagen.fill((0, 0, 0, 0))
        total_piezas_cuerpo = int(
            (ALTO_VENTANA -
             3 * Pajaro.ALTO -
             3 * ParTubo.ALTO_PIEZA) /
            ParTubo.ALTO_PIEZA
        )
        self.piezas_inferiores = randint(1, total_piezas_cuerpo)
        self.piezas_superiores = total_piezas_cuerpo - self.piezas_inferiores

        for i in range(1, self.piezas_inferiores + 1):
            pos_pieza = (0, ALTO_VENTANA - i * ParTubo.ALTO_PIEZA)
            self._imagen.blit(imagen_cuerpo, pos_pieza)
        y_extremo_inferior = ALTO_VENTANA - self.altura_inferior_px
        pos_extremo_inferior = (0, y_extremo_inferior - ParTubo.ALTO_PIEZA)
        self._imagen.blit(imagen_extremo, pos_extremo_inferior)

        for i in range(self.piezas_superiores):
            self._imagen.blit(imagen_cuerpo, (0, i * ParTubo.ALTO_PIEZA))
        y_extremo_superior = self.altura_superior_px
        self._imagen.blit(imagen_extremo, (0, y_extremo_superior))

        self.piezas_superiores += 1
        self.piezas_inferiores += 1
        self._mascara = pygame.mask.from_surface(self._imagen)

    @property
    def altura_superior_px(self):
        return self.piezas_superiores * ParTubo.ALTO_PIEZA

    @property
    def altura_inferior_px(self):
        return self.piezas_inferiores * ParTubo.ALTO_PIEZA

    @property
    def visible(self):
        return -ParTubo.ANCHO < self.x < ANCHO_VENTANA

    @property
    def rectangulo(self):
        return Rect(self.x, 0, ParTubo.ANCHO, ParTubo.ALTO_PIEZA)

    @property
    def rect(self):
        return self.rectangulo

    @property
    def image(self):
        return self._imagen

    @property
    def mask(self):
        return self._mascara

    def actualizar(self, cuadros_delta=1, velocidad=VELOCIDAD_ANIMACION):
        self.x -= velocidad * cuadros_a_mseg(cuadros_delta)

    def colisiona_con(self, pajaro):
        return pygame.sprite.collide_mask(self, pajaro)

def cargar_imagenes():
    def cargar_imagen(nombre_archivo):
        archivo = os.path.join(os.path.dirname(__file__), 'images', nombre_archivo)
        img = pygame.image.load(archivo)
        img.convert()
        return img

    return {
        'fondo': cargar_imagen('background.png'),
        'tubo_base': cargar_imagen('tuberia_final.png'),
        'cuerpo_tubo': cargar_imagen('tuberia_base.png'),
        'bird_up': cargar_imagen('pajaro2.png'),
        'bird_down': cargar_imagen('pajaro1.png')
    }

def cuadros_a_mseg(cuadros, fps=FPS):
    return 1000.0 * cuadros / fps

def mseg_a_cuadros(mseg, fps=FPS):
    return fps * mseg / 1000.0

def principal():
    pygame.init()
    superficie = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption('Juego Testing - Flappy Bird')
    reloj = pygame.time.Clock()
    fuente_puntaje = pygame.font.SysFont(None, 32, bold=True)
    imagenes = cargar_imagenes()
    pajaro = Pajaro(50, int(ALTO_VENTANA / 2 - Pajaro.ALTO / 2), 2,
                    (imagenes['bird_up'], imagenes['bird_down']))
    tubos = deque()
    reloj_cuadros = 0
    puntaje = 0
    terminado = pausado = False

    while not terminado:
        reloj.tick(FPS)
        if not (pausado or reloj_cuadros % mseg_a_cuadros(ParTubo.INTERVALO_AGREGAR)):
            tubos.append(ParTubo(imagenes['tubo_base'], imagenes['cuerpo_tubo']))
        for evento in pygame.event.get():
            if evento.type == QUIT or (evento.type == KEYUP and evento.key == K_ESCAPE):
                terminado = True
                break
            elif evento.type == KEYUP and evento.key in (K_PAUSE, K_p):
                pausado = not pausado
            elif evento.type == MOUSEBUTTONUP or (evento.type == KEYUP and evento.key in (K_UP, K_RETURN, K_SPACE)):
                pajaro.mseg_para_subir = Pajaro.DURACION_SUBIDA
        if pausado:
            continue
        if any(t.colisiona_con(pajaro) for t in tubos) or pajaro.y <= 0 or pajaro.y >= ALTO_VENTANA - Pajaro.ALTO:
            terminado = True
        for x in (0, ANCHO_VENTANA):
            superficie.blit(imagenes['fondo'], (x, 0))
        while tubos and not tubos[0].visible:
            tubos.popleft()
        for t in tubos:
            VELOCIDAD_BASE = VELOCIDAD_ANIMACION + (puntaje // 5) * 0.03
            t.actualizar(velocidad=VELOCIDAD_BASE)
            superficie.blit(t.image, t.rect)
        pajaro.actualizar()
        superficie.blit(pajaro.image, pajaro.rect)
        for t in tubos:
            if t.x + ParTubo.ANCHO < pajaro.x and not t.puntaje_contado:
                puntaje += 1
                t.puntaje_contado = True
        superficie_puntaje = fuente_puntaje.render(str(puntaje), True, (255, 255, 255))
        x_puntaje = ANCHO_VENTANA / 2 - superficie_puntaje.get_width() / 2
        superficie.blit(superficie_puntaje, (x_puntaje, ParTubo.ALTO_PIEZA))
        pygame.display.flip()
        reloj_cuadros += 1

    print('Juego terminado! Puntaje: %i' % puntaje)
    return puntaje

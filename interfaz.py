import pygame
import sys
import os
from flappybird import principal 


ANCHO = 1080
ALTO = 720
FPS = 60

def cargar_fondos():
    ruta = os.path.join(os.path.dirname(__file__), "images")
    return {
        "inicio": pygame.image.load(os.path.join(ruta, "inicio.png")),
        "menu": pygame.image.load(os.path.join(ruta, "menu.png")),
        "instrucciones": pygame.image.load(os.path.join(ruta, "instrucciones.png")),
        "final": pygame.image.load(os.path.join(ruta, "final.png")),
    }

pygame.init()
fondos = cargar_fondos()
fuente_general = pygame.font.SysFont(None, 32, bold=True)
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Flappy Bird - Menú")
fuente = pygame.font.SysFont("arial", 28)
reloj = pygame.time.Clock()

def renderizar_texto_con_borde(texto, fuente, color_texto=(255, 255, 255), color_borde=(0, 0, 0)):
    base = fuente.render(texto, True, color_texto)
    bordes = []

    for dx, dy in [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1),         (0, 1),
                   (1, -1),  (1, 0), (1, 1)]:
        sombra = fuente.render(texto, True, color_borde)
        bordes.append((sombra, dx, dy))

    return base, bordes


def mostrar_texto_centrada(texto, offset_y=0):
    texto_base, bordes = renderizar_texto_con_borde(texto, fuente_general)
    x = ANCHO // 2
    y = ALTO // 2 + offset_y
    for borde, dx, dy in bordes:
        rect = borde.get_rect(center=(x + dx, y + dy))
        ventana.blit(borde, rect)
    rect = texto_base.get_rect(center=(x, y))
    ventana.blit(texto_base, rect)
    return rect

def pantalla_inicio():
    fondo = pygame.transform.scale(fondos["inicio"], (ANCHO, ALTO))
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                return
        ventana.blit(fondo, (0, 0))
        pygame.display.flip()
        reloj.tick(FPS)

def menu():
    fondo = pygame.transform.scale(fondos["menu"], (ANCHO, ALTO))
    while True:
        ventana.blit(fondo, (0, 0))
        r_jugar = mostrar_texto_centrada("Jugar", 0)
        r_instrucciones = mostrar_texto_centrada("Instrucciones", 50)
        r_salir = mostrar_texto_centrada("Salir", 100)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if r_jugar.collidepoint(evento.pos):
                    puntaje = principal()
                    pantalla_final(puntaje)
                elif r_instrucciones.collidepoint(evento.pos):
                    instrucciones()
                elif r_salir.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()


def instrucciones():
    fondo = pygame.transform.scale(fondos["instrucciones"], (ANCHO, ALTO))
    while True:
        ventana.blit(fondo, (0, 0))
        mostrar_texto_centrada("Usa espacio o clic para volar", 0)
        mostrar_texto_centrada("Evita los tubos", 50)
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                return


def pantalla_final(puntaje):
    fondo = pygame.transform.scale(fondos["final"], (ANCHO, ALTO))
    while True:
        ventana.blit(fondo, (0, 0))
        mostrar_texto_centrada(f"PUNTAJE FINAL: {puntaje}", 0)
        r_volver = mostrar_texto_centrada("Volver a jugar", 50)
        r_salir = mostrar_texto_centrada("Salir", 100)
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if r_volver.collidepoint(evento.pos):
                    puntaje = principal()
                    pantalla_final(puntaje)
                elif r_salir.collidepoint(evento.pos):
                    return

if __name__ == "__main__":
    pantalla_inicio()
    menu()
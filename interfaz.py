import pygame
import sys
from flappybird import principal  # Llama a tu juego original

ANCHO = 1920
ALTO = 1080
FPS = 60


pygame.init()
fuente_general = pygame.font.SysFont(None, 32, bold=True)
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Flappy Bird - Menú")
fuente = pygame.font.SysFont("arial", 28)
reloj = pygame.time.Clock()

def mostrar_texto(texto, y):
    render = fuente_general.render(texto, True, (255, 255, 255))
    rect = render.get_rect(center=(ANCHO // 2, y))
    ventana.blit(render, rect)
    return rect

def pantalla_inicio():
    gif = pygame.image.load("images/animacion.gif")
    gif = pygame.transform.scale(gif, (ANCHO, ALTO))
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                return  # Pasa al menú

        ventana.blit(gif, (0, 0))
        pygame.display.flip()
        reloj.tick(FPS)

def menu():
    while True:
        ventana.fill((0, 0, 128))
        titulo = fuente_general.render("FLAPPY BIRD", True, (255, 255, 0))
        ventana.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 50))

        r_jugar = mostrar_texto("1. Jugar", 150)
        r_instrucciones = mostrar_texto("2. Instrucciones", 200)
        r_salir = mostrar_texto("3. Salir", 250)

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
    while True:
        ventana.fill((0, 0, 0))
        mostrar_texto("Usa espacio o clic para volar", 150)
        mostrar_texto("Evita los tubos", 200)
        mostrar_texto("Presiona cualquier tecla para volver", 300)
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                return

def pantalla_final(puntaje):
    while True:
        ventana.fill((0, 0, 0))
        mostrar_texto(f"Puntaje final: {puntaje}", 150)
        r_volver = mostrar_texto("Volver a jugar", 220)
        r_salir = mostrar_texto("Salir", 270)
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
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    pantalla_inicio()
    menu()

import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configuración de ventana
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Recolecta los círculos")

# Colores
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)

# Fuente para mostrar el contador
fuente = pygame.font.Font(None, 36)

# Jugador (rectángulo)
jugador = pygame.Rect(400, 300, 50, 50)
velocidad = 5

# Círculo objetivo
radio = 15
circulo_x = random.randint(radio, ANCHO - radio)
circulo_y = random.randint(radio, ALTO - radio)

# Contador de objetos recogidos
contador = 0

# Bucle principal del juego
reloj = pygame.time.Clock()
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimiento del jugador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jugador.left > 0:
        jugador.x -= velocidad
    if teclas[pygame.K_RIGHT] and jugador.right < ANCHO:
        jugador.x += velocidad
    if teclas[pygame.K_UP] and jugador.top > 0:
        jugador.y -= velocidad
    if teclas[pygame.K_DOWN] and jugador.bottom < ALTO:
        jugador.y += velocidad

    # Detección de colisión
    if jugador.collidepoint(circulo_x, circulo_y):
        contador += 1
        circulo_x = random.randint(radio, ANCHO - radio)
        circulo_y = random.randint(radio, ALTO - radio)

    # Dibujar todo
    ventana.fill(BLANCO)
    pygame.draw.rect(ventana, AZUL, jugador)
    pygame.draw.circle(ventana, ROJO, (circulo_x, circulo_y), radio)

    # Mostrar contador
    texto = fuente.render(f"Objetos recogidos: {contador}", True, NEGRO)
    ventana.blit(texto, (20, 20))

    pygame.display.flip()
    reloj.tick(60)


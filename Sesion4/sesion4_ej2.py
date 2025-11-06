import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de ventana
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pulsacion")

# Colores
BLANCO = (255, 255, 255)
AZUL = (0, 100, 255)

# Parámetros del círculo
x_circulo = ANCHO // 2
y_circulo = ALTO // 2
radio = 20
creciendo = True  # Indica si el círculo está creciendo

# Velocidad de cambio del radio
velocidad = 0.5

# Bucle principal
reloj = pygame.time.Clock()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Actualizar radio del círculo
    if creciendo:
        radio += velocidad
        if radio >= 300:
            creciendo = False
    else:
        radio -= velocidad
        if radio <= 50:
            creciendo = True

    # Dibujar
    ventana.fill(BLANCO)
    pygame.draw.circle(ventana, AZUL, (x_circulo, y_circulo), int(radio))
    pygame.display.flip()

    # Controlar la velocidad de actualización
    reloj.tick(60)


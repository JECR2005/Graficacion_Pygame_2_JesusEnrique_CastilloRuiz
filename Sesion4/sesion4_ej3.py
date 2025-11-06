import pygame
import sys

# Inicializar Pygame
pygame.init()

# Crear ventana vertical (ancho menor que alto)
ANCHO = 400
ALTO = 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Caida con gravedad")

# Colores
BLANCO = (255, 255, 255)
AZUL = (50, 100, 255)

# Propiedades del círculo
radio = 30
x = ANCHO // 2
y = radio
vel_y = 0
gravedad = 0.5
factor_rebote = 0.8  # (reduce velocidad al 80% → pérdida de 20%)

# Control de FPS
clock = pygame.time.Clock()

# Bucle principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Actualizar física
    vel_y += gravedad
    y += vel_y

    # Detectar colisión con el suelo
    if y + radio > ALTO:
        y = ALTO - radio  # reposicionar justo sobre el suelo
        vel_y = -vel_y * factor_rebote  # invertir dirección y perder energía

        # Si el rebote es muy pequeño, detener el movimiento
        if abs(vel_y) < 0.5:
            vel_y = 0

    # Dibujar
    ventana.fill(BLANCO)
    pygame.draw.circle(ventana, AZUL, (x, int(y)), radio)

    # Actualizar pantalla
    pygame.display.flip()

    # Mantener 60 FPS
    clock.tick(60)


import pygame

pygame.init()

# Dimensiones de la ventana
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Rectángulo con aceleración")

# Colores
blanco = (255, 255, 255)
azul = (0, 0, 255)

# Rectángulo
RECT_W, RECT_H = 50, 50
x, y = 400, 300
vel_x, vel_y = 2, 2

# Reloj para controlar FPS
clock = pygame.time.Clock()

corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_a]:  # izquierda
        x -= vel_x
    if teclas[pygame.K_d]:  # derecha
        x += vel_x
    if teclas[pygame.K_w]:  # arriba
        y -= vel_y
    if teclas[pygame.K_s]:  # abajo
        y += vel_y

    # Rebotes y aceleración
    if x <= 0:
        x = 0
        vel_x += 0.1
    elif x >= ANCHO - RECT_W:
        x = ANCHO - RECT_W
        vel_x += 0.1

    if y <= 0:
        y = 0
        vel_y += 0.1
    elif y >= ALTO - RECT_H:
        y = ALTO - RECT_H
        vel_y += 0.1

    # Dibujar
    ventana.fill(blanco)
    pygame.draw.rect(ventana, azul, (x, y, RECT_W, RECT_H))
    pygame.display.flip()

    # Mantener 60 FPS
    clock.tick(60)

pygame.quit()

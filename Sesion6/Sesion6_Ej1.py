import pygame
pygame.init()

# Configuración de ventana
ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Colisión con cambio de color")

# Colores
blanco = (255, 255, 255)
azul = (0, 0, 255)
rojo = (255, 0, 0)
verde = (0, 255, 0)

# Fuente para mostrar texto
font = pygame.font.Font(None, 36)

# Rectángulos
jugador = pygame.Rect(400, 300, 50, 50)
objetivo = pygame.Rect(200, 200, 30, 30)

# Velocidad y control de tiempo
velocidad = 300
clock = pygame.time.Clock()

# Posición flotante para movimiento suave
player_x = float(jugador.x)
player_y = float(jugador.y)

# Color actual del jugador
color_jugador = azul

corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    teclas = pygame.key.get_pressed()
    dt = clock.tick(60) / 1000.0  # tiempo entre frames en segundos

    # Movimiento del jugador
    if teclas[pygame.K_LEFT]:
        player_x -= velocidad * dt
    if teclas[pygame.K_RIGHT]:
        player_x += velocidad * dt
    if teclas[pygame.K_UP]:
        player_y -= velocidad * dt
    if teclas[pygame.K_DOWN]:
        player_y += velocidad * dt

    # Limitar al área de juego
    player_x = max(0, min(800 - jugador.width, player_x))
    player_y = max(0, min(600 - jugador.height, player_y))

    jugador.x = int(player_x)
    jugador.y = int(player_y)

    # Detectar colisión y cambiar color
    if jugador.colliderect(objetivo):
        color_jugador = verde
    else:
        color_jugador = azul

    # Dibujar en pantalla
    ventana.fill(blanco)
    pygame.draw.rect(ventana, color_jugador, jugador)
    pygame.draw.rect(ventana, rojo, objetivo)

    # Mostrar texto si hay colisión
    if jugador.colliderect(objetivo):
        texto = font.render("¡Colisión!", True, (0, 0, 0))
        rect_texto = texto.get_rect(center=(ventana.get_width() // 2, 30))
        ventana.blit(texto, rect_texto)

    pygame.display.flip()

pygame.quit()

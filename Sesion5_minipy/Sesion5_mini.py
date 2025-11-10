import pygame
import sys
import math

pygame.init()

# ===========================
# CONFIGURACIÓN INICIAL
# ===========================
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Sprite que rota hacia el ratón o joystick")

# Cargar sprite (una sola imagen)
sprite = pygame.image.load("Sesion5_minipy/Super_Mario.jpg").convert_alpha()

# Escalar imagen (ajustar tamaño)
escala = 4
sprite = pygame.transform.scale(sprite, (sprite.get_width() // 10 * escala, sprite.get_height() // 8 * escala))

# Posición inicial (centro)
x, y = ANCHO // 2, ALTO // 2
velocidad = 5
angulo = 0

# Configurar joystick (si existe)
pygame.joystick.init()
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick detectado: {joystick.get_name()}")

clock = pygame.time.Clock()

# ===========================
# BUCLE PRINCIPAL
# ===========================
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # ===========================
    # OBTENER DIRECCIÓN AL RATÓN
    # ===========================
    mx, my = pygame.mouse.get_pos()
    dx = mx - x
    dy = my - y
    angulo = math.degrees(math.atan2(-dy, dx))  # atan2 usa y negativo porque el eje Y crece hacia abajo

    # ===========================
    # ENTRADAS DE TECLADO Y JOYSTICK
    # ===========================
    teclas = pygame.key.get_pressed()
    mover = teclas[pygame.K_w]

    if joystick:
        # Botón 0 (A en Xbox, X en PS)
        if joystick.get_button(0):
            mover = True

    # ===========================
    # MOVIMIENTO HACIA ADELANTE
    # ===========================
    if mover:
        # Convertir ángulo a radianes para movimiento
        rad = math.radians(angulo)
        x += math.cos(rad) * velocidad
        y -= math.sin(rad) * velocidad

    # Evitar salir de la ventana
    x = max(0, min(x, ANCHO))
    y = max(0, min(y, ALTO))

    # ===========================
    # DIBUJAR
    # ===========================
    ventana.fill((25, 25, 40))

    # Rotar sprite hacia el ratón
    sprite_rotado = pygame.transform.rotate(sprite, angulo)
    rect = sprite_rotado.get_rect(center=(x, y))
    ventana.blit(sprite_rotado, rect.topleft)

    # Mostrar línea al ratón (opcional)
    pygame.draw.line(ventana, (255, 255, 0), (x, y), (mx, my), 1)

    pygame.display.flip()
    clock.tick(60)


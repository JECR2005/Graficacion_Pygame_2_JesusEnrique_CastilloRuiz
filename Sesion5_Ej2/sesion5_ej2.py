import pygame
import sys

pygame.init()

# Configuración de ventana
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Sprite Controlado")

# Cargar hoja de sprites
sprite_sheet = pygame.image.load("Sesion5_Ej2/cat_sprite1.png").convert_alpha()

# Configuración de la hoja (10 columnas x 8 filas)
cols = 10
rows = 8
frame_ancho = sprite_sheet.get_width() // cols
frame_alto = sprite_sheet.get_height() // rows

# Margen para evitar sangrado visual (1 píxel arriba y abajo)
margen = 1

# Seleccionar la fila (0 = primera fila) 0-4
fila = 0

# Extraer frames con corrección de borde
frames = []
for i in range(cols):
    x = i * frame_ancho
    y = fila * frame_alto + margen
    frame = sprite_sheet.subsurface((x, y, frame_ancho, frame_alto - margen * 2))
    escala = 4
    frame_escalado = pygame.transform.scale(frame, (frame_ancho * escala, (frame_alto - margen * 2) * escala))
    frames.append(frame_escalado)

# Control de animación
indice_frame = 0
tiempo_cambio = 100
ultimo_cambio = pygame.time.get_ticks()

# Posición y movimiento
x = ANCHO // 2
y = ALTO - frames[0].get_height() - 20
velocidad = 5
direccion = "derecha"
moviendo = False

clock = pygame.time.Clock()

# Bucle principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()
    moviendo = False

    if teclas[pygame.K_a]:
        x -= velocidad
        direccion = "izquierda"
        moviendo = True
    if teclas[pygame.K_d]:
        x += velocidad
        direccion = "derecha"
        moviendo = True

    # Evitar que salga de la ventana
    if x < 0:
        x = 0
    if x + frames[0].get_width() > ANCHO:
        x = ANCHO - frames[0].get_width()

    # Animación solo si se mueve
    tiempo_actual = pygame.time.get_ticks()
    if moviendo and tiempo_actual - ultimo_cambio > tiempo_cambio:
        indice_frame = (indice_frame + 1) % len(frames)
        ultimo_cambio = tiempo_actual
    elif not moviendo:
        indice_frame = 0

    frame_actual = frames[indice_frame]

    if direccion == "izquierda":
        frame_actual = pygame.transform.flip(frame_actual, True, False)

    ventana.fill((20, 20, 35))
    ventana.blit(frame_actual, (x, y))
    pygame.display.flip()
    clock.tick(60)

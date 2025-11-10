import pygame
import sys
import random

pygame.init()

# Configuración de ventana
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Evita los Círculos")

# Fuentes
fuente = pygame.font.Font(None, 74)
fuente_peque = pygame.font.Font(None, 36)

# Cargar hoja de sprites
sprite_sheet = pygame.image.load("Sesion5_Ej2/cat_sprite1.png").convert_alpha()

# Configuración de la hoja (10 columnas x 8 filas)
cols = 10
rows = 8
frame_ancho = sprite_sheet.get_width() // cols
frame_alto = sprite_sheet.get_height() // rows
margen = 1
fila = 0  # fila de animación (puedes cambiarla)

# Extraer y escalar frames
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

# Parámetros del jugador
velocidad = 7
direccion = "derecha"
moviendo = False

# Función para reiniciar el juego
def reiniciar():
    jugador = pygame.Rect(ANCHO//2, ALTO - frames[0].get_height() - 20, frames[0].get_width(), frames[0].get_height())
    enemigos = []
    for _ in range(5):
        enemigo = {
            "x": random.randint(50, ANCHO - 50),
            "y": random.randint(-400, -50),
            "radio": random.randint(20, 35),
            "vel": random.randint(3, 6)
        }
        enemigos.append(enemigo)
    return jugador, enemigos

jugador, enemigos = reiniciar()
clock = pygame.time.Clock()

# Estado del juego
estado = "jugando"
tiempo_derrota = 0
inicio_tiempo = pygame.time.get_ticks()  # tiempo inicial

# Bucle principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if estado == "jugando":
        teclas = pygame.key.get_pressed()
        moviendo = False

        # Movimiento horizontal
        if teclas[pygame.K_a]:
            jugador.x -= velocidad
            direccion = "izquierda"
            moviendo = True
        if teclas[pygame.K_d]:
            jugador.x += velocidad
            direccion = "derecha"
            moviendo = True

        # Límites
        if jugador.x < 0:
            jugador.x = 0
        if jugador.x + jugador.width > ANCHO:
            jugador.x = ANCHO - jugador.width

        # Animación
        tiempo_actual = pygame.time.get_ticks()
        if moviendo and tiempo_actual - ultimo_cambio > tiempo_cambio:
            indice_frame = (indice_frame + 1) % len(frames)
            ultimo_cambio = tiempo_actual
        elif not moviendo:
            indice_frame = 0

        frame_actual = frames[indice_frame]
        if direccion == "izquierda":
            frame_actual = pygame.transform.flip(frame_actual, True, False)

        # Mover enemigos
        for enemigo in enemigos:
            enemigo["y"] += enemigo["vel"]
            if enemigo["y"] > ALTO + enemigo["radio"]:
                enemigo["y"] = random.randint(-400, -50)
                enemigo["x"] = random.randint(50, ANCHO - 50)
                enemigo["vel"] = random.randint(3, 6)

        # Colisiones
        colision = False
        for enemigo in enemigos:
            dx = jugador.centerx - enemigo["x"]
            dy = jugador.centery - enemigo["y"]
            distancia = (dx**2 + dy**2)**0.5
            if distancia < enemigo["radio"] + jugador.width/3:
                colision = True
                break

        if colision:
            estado = "derrota"
            tiempo_derrota = pygame.time.get_ticks()

        # Calcular tiempo vivo
        tiempo_vivo_ms = pygame.time.get_ticks() - inicio_tiempo
        segundos = (tiempo_vivo_ms // 1000) % 60
        minutos = (tiempo_vivo_ms // 60000)
        texto_tiempo = fuente_peque.render(f"Tiempo vivo: {minutos:02}:{segundos:02}", True, (255, 255, 255))

        # Dibujar
        ventana.fill((20, 20, 35))
        for enemigo in enemigos:
            pygame.draw.circle(ventana, (255, 0, 0), (enemigo["x"], enemigo["y"]), enemigo["radio"])
        ventana.blit(frame_actual, (jugador.x, jugador.y))
        ventana.blit(texto_tiempo, (ANCHO - texto_tiempo.get_width() - 20, 20))

    elif estado == "derrota":
        ventana.fill((10, 10, 25))
        texto = fuente.render("¡Has perdido!", True, (255, 50, 50))
        subtexto = fuente_peque.render("Reiniciando...", True, (255, 255, 255))
        ventana.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2 - 50))
        ventana.blit(subtexto, (ANCHO//2 - subtexto.get_width()//2, ALTO//2 + 20))

        # Reiniciar después de 5 segundos
        if pygame.time.get_ticks() - tiempo_derrota > 5000:
            jugador, enemigos = reiniciar()
            estado = "jugando"
            inicio_tiempo = pygame.time.get_ticks()  # reinicia el contador

    pygame.display.flip()
    clock.tick(60)

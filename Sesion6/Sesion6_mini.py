import pygame
import sys
import random

pygame.init()

# Configuración de ventana
ANCHO, ALTO = 800, 800
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Evita los Círculos")

# Cargar hoja de sprites
sprite_sheet = pygame.image.load("Sesion5_Ej2/cat_sprite1.png").convert_alpha()

# Configuración de la hoja (10 columnas x 8 filas)
cols = 10
rows = 8
frame_ancho = sprite_sheet.get_width() // cols
frame_alto = sprite_sheet.get_height() // rows

margen = 1
fila = 0
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

# Posición y movimiento del jugador
x = ANCHO // 2
y = ALTO - frames[0].get_height() - 20
velocidad = 5
direccion = "derecha"
moviendo = False

# Enemigos
enemigos = []
for _ in range(3):  # empieza con pocos
    enemigos.append({
        "x": random.randint(0, ANCHO),
        "y": random.randint(-300, -50),
        "r": 25,
        "vel": random.uniform(1.5, 3.0)
    })

# Puntos azules
puntos = []
ultimo_spawn_punto = pygame.time.get_ticks()
spawn_intervalo = 3000  # cada 3 segundos
duracion_punto = 5000   # desaparece después de 5 s

# Variables de juego
reloj = pygame.time.Clock()
font = pygame.font.Font(None, 36)
inicio_tiempo = pygame.time.get_ticks()
puntuacion = 0
game_over = False
tiempo_derrota = 0
tiempo_vivo = 0
puntuacion_final = 0

# Función para reiniciar el juego
def reiniciar():
    global enemigos, inicio_tiempo, puntuacion, game_over, tiempo_derrota, puntos, x, tiempo_vivo, puntuacion_final
    enemigos = []
    for _ in range(3):
        enemigos.append({
            "x": random.randint(0, ANCHO),
            "y": random.randint(-300, -50),
            "r": 25,
            "vel": random.uniform(1.5, 3.0)
        })
    x = ANCHO // 2
    puntuacion = 0
    puntos = []
    inicio_tiempo = pygame.time.get_ticks()
    game_over = False
    tiempo_derrota = 0
    tiempo_vivo = 0
    puntuacion_final = 0

# Bucle principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()

    if not game_over:
        moviendo = False
        if teclas[pygame.K_a]:
            x -= velocidad
            direccion = "izquierda"
            moviendo = True
        if teclas[pygame.K_d]:
            x += velocidad
            direccion = "derecha"
            moviendo = True

        # Limitar movimiento
        if x < 0:
            x = 0
        if x + frames[0].get_width() > ANCHO:
            x = ANCHO - frames[0].get_width()

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

        # Tiempo y dificultad progresiva
        tiempo_vivo = (tiempo_actual - inicio_tiempo) // 1000
        dificultad = 1 + (tiempo_vivo // 10) * 0.25  # cada 10 seg aumenta un 25%
        velocidad_enemigo = 2.0 * dificultad

        # Aumentar cantidad de enemigos con el tiempo (máx 10)
        if len(enemigos) < 10 and tiempo_vivo % 15 == 0 and tiempo_vivo > 0:
            enemigos.append({
                "x": random.randint(0, ANCHO),
                "y": random.randint(-300, -50),
                "r": 25,
                "vel": random.uniform(2, 4) * dificultad
            })

        # Mover enemigos
        for e in enemigos:
            e["y"] += e["vel"]
            if e["y"] > ALTO:
                e["y"] = random.randint(-100, -40)
                e["x"] = random.randint(0, ANCHO)
                e["vel"] = random.uniform(1.5, 3.5) * dificultad

        # Generar puntos azules (más arriba)
        if tiempo_actual - ultimo_spawn_punto > spawn_intervalo:
            puntos.append({
                "x": random.randint(50, ANCHO - 50),
                "y": random.randint(ALTO - 220, ALTO - 120),
                "spawn": tiempo_actual
            })
            ultimo_spawn_punto = tiempo_actual

        # Eliminar puntos caducados
        puntos = [p for p in puntos if tiempo_actual - p["spawn"] < duracion_punto]

        # Colisiones
        jugador_rect = pygame.Rect(x, y, frame_actual.get_width(), frame_actual.get_height())
        for e in enemigos:
            dist = ((x + frame_actual.get_width() // 2 - e["x"]) ** 2 +
                    (y + frame_actual.get_height() // 2 - e["y"]) ** 2) ** 0.5
            if dist < e["r"] + frame_actual.get_width() // 2.5:
                game_over = True
                tiempo_derrota = pygame.time.get_ticks()
                puntuacion_final = puntuacion
                break

        # Colisión con puntos
        for p in puntos[:]:
            if jugador_rect.collidepoint(p["x"], p["y"]):
                puntos.remove(p)
                puntuacion += 1

        # Dibujar
        ventana.fill((20, 20, 35))
        for e in enemigos:
            pygame.draw.circle(ventana, (255, 0, 0), (e["x"], int(e["y"])), e["r"])
        for p in puntos:
            pygame.draw.circle(ventana, (0, 100, 255), (p["x"], p["y"]), 8)

        ventana.blit(frame_actual, (x, y))

        # Mostrar tiempo vivo y puntuación
        minutos = tiempo_vivo // 60
        segundos = tiempo_vivo % 60
        texto_tiempo = font.render(f"Tiempo vivo: {minutos:02}:{segundos:02}", True, (255, 255, 255))
        texto_puntos = font.render(f"Puntuación: {puntuacion}", True, (0, 150, 255))
        ventana.blit(texto_tiempo, (ANCHO - 260, 10))
        ventana.blit(texto_puntos, (ANCHO - 260, 50))

    else:
        ventana.fill((10, 10, 20))
        texto = font.render("¡Has perdido!", True, (255, 80, 80))
        texto_tiempo_final = font.render(f"Tiempo sobrevivido: {tiempo_vivo // 60:02}:{tiempo_vivo % 60:02}", True, (255, 255, 255))
        texto_puntos_final = font.render(f"Puntuación final: {puntuacion_final}", True, (0, 150, 255))
        ventana.blit(texto, (ANCHO // 2 - 100, ALTO // 2 - 60))
        ventana.blit(texto_tiempo_final, (ANCHO // 2 - 130, ALTO // 2))
        ventana.blit(texto_puntos_final, (ANCHO // 2 - 110, ALTO // 2 + 40))

        # Reiniciar después de 3 segundos
        if pygame.time.get_ticks() - tiempo_derrota > 3000:
            reiniciar()

    pygame.display.flip()
    reloj.tick(60)

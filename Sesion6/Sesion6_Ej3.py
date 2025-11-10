import pygame
import random
import sys

# Inicializar pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 400, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Flappy Pobre")

# Colores
AZUL = (135, 206, 235)
VERDE = (0, 200, 0)
MARRON = (160, 82, 45)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Fuente
fuente = pygame.font.Font(None, 36)
grande = pygame.font.Font(None, 60)

# Parámetros del juego
gravedad = 0.5
salto = -8
vel_tuberia = 3.0
espacio_tuberia = 150
distancia_tuberias = 250
ancho_tuberia = 60

# Configuración del pájaro
bird = pygame.Rect(100, ALTO // 2, 34, 24)
vel_y = 0

# Lista de obstáculos: cada elemento será un dict {top, bottom, coin}
obstaculos = []

# Puntuación
puntuacion = 0
juego_activo = True
tiempo = 0
reloj = pygame.time.Clock()

def crear_obstaculo():
    """Crea una pareja de tuberías y una moneda entre ellas (cada obstáculo es un dict)."""
    altura_centro = random.randint(espacio_tuberia + 50, ALTO - 100)
    top_rect = pygame.Rect(ANCHO, 0, ancho_tuberia, altura_centro - espacio_tuberia // 2)
    bottom_rect = pygame.Rect(ANCHO, altura_centro + espacio_tuberia // 2, ancho_tuberia, ALTO - (altura_centro + espacio_tuberia // 2))
    # Colocar la moneda en el centro vertical entre las tuberías
    coin_x = ANCHO + ancho_tuberia // 2 - 10
    coin_y = altura_centro
    coin_rect = pygame.Rect(coin_x, coin_y - 10, 20, 20)  # 20x20 rect para la moneda
    obstaculos.append({'top': top_rect, 'bottom': bottom_rect, 'coin': coin_rect})

def dibujar_tuberias():
    for obs in obstaculos:
        pygame.draw.rect(ventana, VERDE, obs['top'])
        pygame.draw.rect(ventana, VERDE, obs['bottom'])
        pygame.draw.rect(ventana, MARRON, obs['top'], 3)
        pygame.draw.rect(ventana, MARRON, obs['bottom'], 3)

def dibujar_objetos():
    for obs in obstaculos:
        coin = obs['coin']
        if coin:  # coin puede eliminarse (setear a None) tras recogerla
            pygame.draw.circle(ventana, AMARILLO, coin.center, 10)

def reiniciar_juego():
    global bird, vel_y, obstaculos, puntuacion, juego_activo, tiempo, vel_tuberia
    bird.y = ALTO // 2
    vel_y = 0
    obstaculos.clear()
    puntuacion = 0
    tiempo = 0
    vel_tuberia = 3.0
    crear_obstaculo()
    juego_activo = True

# Crear primer obstáculo
crear_obstaculo()

# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if juego_activo:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                vel_y = salto
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reiniciar_juego()

    if juego_activo:
        # Lógica del pájaro
        vel_y += gravedad
        bird.y += vel_y

        # Mover tuberías y monedas
        for obs in obstaculos:
            obs['top'].x -= vel_tuberia
            obs['bottom'].x -= vel_tuberia
            if obs['coin'] is not None:
                obs['coin'].x -= vel_tuberia

        # Agregar nueva tubería cuando la última haya avanzado lo suficiente
        if obstaculos and obstaculos[-1]['top'].x < ANCHO - distancia_tuberias:
            crear_obstaculo()

        # Eliminar obstáculos fuera de pantalla (por la izquierda)
        # Usamos una nueva lista para evitar problemas al eliminar mientras iteramos
        obstaculos = [obs for obs in obstaculos if obs['top'].x + ancho_tuberia > 0]

        # Verificar colisiones con tuberías
        for obs in obstaculos:
            if bird.colliderect(obs['top']) or bird.colliderect(obs['bottom']):
                juego_activo = False
                break

        # Recolectar monedas: iterar sobre copia o sobre la lista y modificar el dict
        for obs in obstaculos:
            coin = obs['coin']
            if coin is not None and bird.colliderect(coin):
                obs['coin'] = None   # quitar la moneda para que no se vuelva a contar
                puntuacion += 1

        # También eliminar monedas que salieron de la pantalla por la izquierda (seguridad)
        for obs in obstaculos:
            coin = obs['coin']
            if coin is not None and coin.x + coin.width < 0:
                obs['coin'] = None

        # Verificar límites superior/inferior del pájaro
        if bird.y > ALTO or bird.y + bird.height < 0:
            juego_activo = False

        # Aumentar dificultad con el tiempo
        tiempo += 1
        if tiempo % 1000 == 0:
            vel_tuberia += 0.3

    # Dibujar escena
    ventana.fill(AZUL)
    pygame.draw.rect(ventana, VERDE, (0, ALTO - 30, ANCHO, 30))
    pygame.draw.ellipse(ventana, ROJO, bird)
    dibujar_tuberias()
    dibujar_objetos()

    if juego_activo:
        texto = fuente.render(f"Puntos: {puntuacion}", True, BLANCO)
        ventana.blit(texto, (10, 10))
    else:
        texto_final = grande.render("GAME OVER", True, ROJO)
        ventana.blit(texto_final, (ANCHO // 2 - 150, ALTO // 2 - 60))
        texto_punt = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)
        ventana.blit(texto_punt, (ANCHO // 2 - 80, ALTO // 2))
        texto_reinicio = fuente.render("Presiona ESPACIO para reiniciar", True, BLANCO)
        ventana.blit(texto_reinicio, (ANCHO // 2 - 170, ALTO // 2 + 40))

    pygame.display.flip()
    reloj.tick(60)

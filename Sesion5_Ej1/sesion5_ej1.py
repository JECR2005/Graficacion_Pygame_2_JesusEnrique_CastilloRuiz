import pygame

# Inicializar Pygame
pygame.init()
ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Imagen con cambio de tamaño")

# Colores
blanco = (255, 255, 255)

# Variables de posición y movimiento
x, y = 400, 300
velocidad_x = 5

# Tamaño inicial
escala = 1.0  # 1.0 = 100% del tamaño original

# Cargar imagen (usa tu propia ruta o nombre de archivo)
imagen_original = pygame.image.load("Sesion5_Ej1/ConfuseJane.jpg").convert_alpha()  # Mantiene transparencia
ancho_original, alto_original = imagen_original.get_size()
imagen = imagen_original.copy()

# Control de FPS
reloj = pygame.time.Clock()
corriendo = True

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    teclas = pygame.key.get_pressed()

    # Aumentar tamaño (E)
    if teclas[pygame.K_e]:
        escala += 0.02
        if escala > 3.0:
            escala = 3.0

    # Disminuir tamaño (Q)
    if teclas[pygame.K_q]:
        escala -= 0.02
        if escala < 0.3:
            escala = 0.3

    # Actualizar tamaño de la imagen (manteniendo proporciones)
    ancho = int(ancho_original * escala)
    alto = int(alto_original * escala)
    imagen = pygame.transform.scale(imagen_original, (ancho, alto))

    # Movimiento horizontal
    x += velocidad_x
    if x > 800 - ancho // 2 or x < ancho // 2:
        velocidad_x = -velocidad_x

    # Dibujar
    ventana.fill(blanco)
    ventana.blit(imagen, (x - ancho // 2, y - alto // 2))  # Centrado
    pygame.display.flip()

    # Controlar FPS
    reloj.tick(60)

pygame.quit()

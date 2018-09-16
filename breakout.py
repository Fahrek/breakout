import sys  # para usar exit()
import pygame

WIDTH = 640
HEIGHT = 480
bgBlueCol = (0, 0, 64)  # Color azul para el fondo


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        self.image = pygame.image.load('assets/ball.png')
        # Obtener rectangulo de la imagen
        self.rect = self.image.get_rect()
        # Posicion inicial centrada en pantalla
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        # Establecer velocidad inicial
        self.speed = [3, 3]

    def update(self):
        # Evitar que salga por arriba y por abajo
        if self.rect.bottom >= HEIGHT or self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
        # Evitar que salga por la derecha y por la izquierda
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]
        # Mover en base a posicion actual y velocidad
        self.rect.move_ip(self.speed)


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        self.image = pygame.image.load('assets/paddle.png')
        # Obtener rectangulo de la imagen
        self.rect = self.image.get_rect()
        # Posicion inicial centrada en pantalla en X
        self.rect.midbottom = (WIDTH / 2, HEIGHT - 20)
        # Establecer velocidad inicial
        self.speed = [0, 0]

    def update(self, evento):
        # Buscar si se presionó flecha izquierda
        if evento.key == pygame.K_LEFT and self.rect.left > 0:
            self.speed = [-5, 0]
        # Buscar si se presionó flecha derecha
        elif evento.key == pygame.K_RIGHT and self.rect.right < WIDTH:
            self.speed = [5, 0]
        else:
            self.speed = [0, 0]
        # Mover en base a posicion actual y velocidad
        self.rect.move_ip(self.speed)

# Inicializando pantalla


screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Configurar título de la pantalla
pygame.display.set_caption('BreakOut')
# Crear el reloj
clock = pygame.time.Clock()
# Ajustar repetición de evento de tecla presionada
pygame.key.set_repeat(30)

ball = Ball()
player = Paddle()

while True:
    # Establecer FPS
    clock.tick(60)
    # Revisar todos los eventos
    for evento in pygame.event.get():
        # Si se presiona la cruz de la barra de titulo,
        if evento.type == pygame.QUIT:
            # cerrar el videojuego
            sys.exit()
        # Buscar eventos del teclado,
        elif evento.type == pygame.KEYDOWN:
            player.update(evento)

    # Actualizar la posicion de la bola
    ball.update()

    # Rellenar fondo de pantalla con el color azul
    screen.fill(bgBlueCol)
    # Dibujar bola en pantalla
    screen.blit(ball.image, ball.rect)
    # Dibujar jugador en pantalla
    screen.blit(player.image, player.rect)
    # Actualizar los elementos en pantalla
    pygame.display.flip()

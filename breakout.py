import sys  # para usar exit()
import time  # para usar sleep()
import pygame

WIDTH = 640
HEIGHT = 480
bgBlueCol = (0, 0, 64)  # Color azul para el fondo
white_color = (255, 255, 255)  # Color blanco para textos

pygame.init()

class Scene:
    def __init__(self):
        "Initialization"
        self.nextScene = False
        self.playing = True

    def read_events(self, events):
        "Lee la lista de los todos eventos"
        pass

    def update(self):
        "Calculos y logica"
        pass

    def render(self, screen):
        "Dibujar los objetos en pantalla"
        pass

    def change_scene(self, scene):
        "Selecciona la nueva escena a ser desplegada"
        self.nextScene = scene


class Director:
    def __init__(self, title = "", res = (WIDTH, HEIGHT)):
        pygame.init()
        self.screen = pygame.display.set_mode(res)
        # Configurar título de la pantalla
        pygame.display.set_caption(title)
        # Crear el reloj
        self.clock = pygame.time.Clock()
        self.scene = None
        self.scenes = {}

    def execute(self, init_scene, fps = 60):
        self.scene = self.scenes[init_scene]
        playing = True
        while playing:
            self.clock.tick(fps)
            events = pygame.event.get()
            # Revisar todos los eventos
            for event in events:
                # Si se presiona la cruz de la barra de titulo,
                if event.type == pygame.QUIT:
                    # cerrar el videojuego
                    playing = False

            self.scene.read_events(events)
            self.scene.update()
            self.scene.render(self.screen)

            self.choiceScene(self.scene.nextScene)

            if playing:
                playing = self.scene.playing

            pygame.display.flip()

        time.sleep(3)

    def choiceScene(self, nextScene):
        if nextScene:
            if nextScene not in self.scenes:
                self.addScene(nextScene)
            self.scene = self.scenes[nextScene]

    def addScene(self, scene):
        sceneClass = 'STAGE' + scene
        sceneObj = globals()[sceneClass]
        self.scenes[scene] = sceneObj()


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
        if self.rect.top <= 0:
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

    def update(self, event):
        # Buscar si se presionó flecha izquierda
        if event.key == pygame.K_LEFT and self.rect.left > 0:
            self.speed = [-5, 0]
        # Buscar si se presionó flecha derecha
        elif event.key == pygame.K_RIGHT and self.rect.right < WIDTH:
            self.speed = [5, 0]
        else:
            self.speed = [0, 0]
        # Mover en base a posicion actual y velocidad
        self.rect.move_ip(self.speed)


class Brick(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        self.image = pygame.image.load('assets/brick.png')
        # Obtener rectangulo de la imagen
        self.rect = self.image.get_rect()
        # Posicion inicial, provista externamente
        self.rect.topleft = position


class Wall(pygame.sprite.Group):
    def __init__(self, qBricks):
        pygame.sprite.Group.__init__(self)

        pos_x = 0
        pos_y = 20
        for i in range(qBricks):
            brick = Brick((pos_x, pos_y))
            self.add(brick)

            pos_x += brick.rect.width
            if pos_x >= WIDTH:
                pos_x = 0
                pos_y += brick.rect.height

# Funcion llamada tras dejar ir la bola


def game_over():
    font = pygame.font.SysFont('Arial', 72)
    text = font.render('GAME OVER :(', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = [WIDTH / 2, HEIGHT / 2]
    screen.blit(text, text_rect)
    pygame.display.flip()
    # Pausar por tres segundos
    time.sleep(3)
    # Salir
    sys.exit()


def show_points():
    font = pygame.font.SysFont('Consolas', 20)
    text = font.render(str(points).zfill(5), True, white_color)
    text_rect = text.get_rect()
    text_rect.topleft = [0, 0]
    screen.blit(text, text_rect)


def show_lives():
    font = pygame.font.SysFont('Consolas', 20)
    chain = "Vidas: " + str(lives).zfill(2)
    text = font.render(chain, True, white_color)
    text_rect = text.get_rect()
    text_rect.topright = [WIDTH, 0]
    screen.blit(text, text_rect)


# Inicializando pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Configurar título de la pantalla
pygame.display.set_caption('BreakOut')
# Crear el reloj
clock = pygame.time.Clock()
# Ajustar repetición de evento de tecla presionada
pygame.key.set_repeat(30)


# Instanciando objetos en pantalla

ball = Ball()
player = Paddle()
wall = Wall(50)
points = 0
lives = 3
waiting_tOut = True

while True:
    # Establecer FPS
    clock.tick(60)
    # Revisar todos los eventos
    for event in pygame.event.get():
        # Si se presiona la cruz de la barra de titulo,
        if event.type == pygame.QUIT:
            # cerrar el videojuego
            sys.exit()
        # Buscar eventos del teclado,
        elif event.type == pygame.KEYDOWN:
            player.update(event)
            if waiting_tOut == True and event.key == pygame.K_SPACE:
                waiting_tOut = False
                if ball.rect.centerx < WIDTH / 2:
                    ball.speed = [3, -3]
                else:
                    ball.speed = [-3, -3]


    # Actualizar la posicion de la bola
    if waiting_tOut == False:
        ball.update()
    else:
        ball.rect.midbottom = player.rect.midtop

    # Colision entre la bola y el jugador
    if pygame.sprite.collide_rect(ball, player):
        ball.speed[1] = -ball.speed[1]

    # Colision de la bola con el muro
    list = pygame.sprite.spritecollide(ball, wall, False)
    if list:
        brick = list[0]
        cx = ball.rect.centerx
        if cx < brick.rect.left or cx > brick.rect.right:
            ball.speed[0] = -ball.speed[0]
        else:
            ball.speed[1] = -ball.speed[1]
        wall.remove(brick)
        points += 10

    # Revisar si la bola sale de la pantalla
    if ball.rect.top > HEIGHT:
        lives -= 1
        waiting_tOut = True

    # Rellenar fondo de pantalla con el color azul
    screen.fill(bgBlueCol)
    # Mostrar puntuacion
    show_points()
    # Mostrar vidas
    show_lives()
    # Dibujar bola en pantalla
    screen.blit(ball.image, ball.rect)
    # Dibujar jugador en pantalla
    screen.blit(player.image, player.rect)
    # Dibujar los ladrillos
    wall.draw(screen)
    # Actualizar los elementos en pantalla
    pygame.display.flip()

    if lives <= 0:
        game_over()

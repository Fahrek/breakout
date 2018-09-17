import sys  # para usar exit()
import time  # para usar sleep()
import pygame

WIDTH = 640  # Ancho de la pantalla.
HEIGHT = 480  # Alto de la pantalla.
bgBlueCol = (0, 0, 64)  # Color azul para el fondo
white_color = (255, 255, 255)  # Color blanco para textos


class Scene:
    "Esqueleto para cada una de las escenas del videojuego."
    def __init__(self):
        "Inicializacion"
        self.nextScene = False
        self.playing = True

    def read_events(self, events):
        "Lee los eventos para interactuar con los objetos."
        pass

    def update(self):
        "Calculos y logica. Actualiza los objetos en la pantalla."
        pass

    def render(self, screen):
        "Dibuja los objetos en pantalla"
        pass

    def change_scene(self, scene):
        "Selecciona la nueva escena a ser desplegada. Cambia la escena de juego"
        self.nextScene = scene


class Director:
    def __init__(self, title="", res=(WIDTH, HEIGHT)):
        pygame.init()
        # Inicializando pantalla
        self.screen = pygame.display.set_mode(res)
        # Configurar titulo de la pantalla
        pygame.display.set_caption(title)
        # Crear el reloj
        self.clock = pygame.time.Clock()
        self.scene = None
        self.scenes = {}

    def execute(self, init_scene, fps=60):
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

            # Actualizar los elementos en pantalla
            pygame.display.flip()

        time.sleep(3)

    def choiceScene(self, nextScene):
        if nextScene:
            if nextScene not in self.scenes:
                self.addScene(nextScene)
            self.scene = self.scenes[nextScene]

    def addScene(self, scene):
        sceneClass = 'Scene' + scene
        sceneObj = globals()[sceneClass]
        self.scenes[scene] = sceneObj()


class SceneStage1(Scene):
    def __init__(self):
        Scene.__init__(self)

        self.ball = Ball()
        self.player = Paddle()
        self.wall = Wall(50)

        self.points = 0
        self.lives = 3
        self.waiting_tOut = True

        # Ajustar repeticion de evento de tecla presionada
        pygame.key.set_repeat(30)

    def read_events(self, events):
        for event in events:
            # Buscar eventos del teclado,
            if event.type == pygame.KEYDOWN:
                self.player.update(event)
                if self.waiting_tOut == True and event.key == pygame.K_SPACE:
                    self.waiting_tOut = False
                    if self.ball.rect.centerx < WIDTH / 2:
                        self.ball.speed = [3, -3]
                    else:
                        self.ball.speed = [-3, -3]

    def update(self):
        # Actualizar la posicion de la bola (OJO: if self.waiting_tOut == False:)
        if not self.waiting_tOut:
            self.ball.update()
        else:
            self.ball.rect.midbottom = self.player.rect.midtop

        # Colision entre la bola y el jugador
        if pygame.sprite.collide_rect(self.ball, self.player):
            self.ball.speed[1] = -self.ball.speed[1]

        # Colision de la bola con el muro
        list = pygame.sprite.spritecollide(self.ball, self.wall, False)
        if list:
            brick = list[0]
            cx = self.ball.rect.centerx
            if cx < brick.rect.left or cx > brick.rect.right:
                self.ball.speed[0] = -self.ball.speed[0]
            else:
                self.ball.speed[1] = -self.ball.speed[1]
            self.wall.remove(brick)
            self.points += 10

        # Revisar si la bola sale de la pantalla
        if self.ball.rect.top > HEIGHT:
            self.lives -= 1
            self.waiting_tOut = True

        if self.lives <= 0:
            self.change_scene('GameOver')

    def render(self, screen):
        # Rellenar fondo de pantalla con el color azul
        screen.fill(bgBlueCol)
        # Mostrar puntuacion
        self.show_points(screen)
        # Mostrar vidas
        self.show_lives(screen)
        # Dibujar bola en pantalla
        screen.blit(self.ball.image, self.ball.rect)
        # Dibujar jugador en pantalla
        screen.blit(self.player.image, self.player.rect)
        # Dibujar los ladrillos
        self.wall.draw(screen)

    def show_points(self, screen):
        font = pygame.font.SysFont('Consolas', 20)
        text = font.render(str(self.points).zfill(5), True, white_color)
        text_rect = text.get_rect()
        text_rect.topleft = [0, 0]
        screen.blit(text, text_rect)

    def show_lives(self, screen):
        font = pygame.font.SysFont('Consolas', 20)
        chain = "Vidas: " + str(self.lives).zfill(2)
        text = font.render(chain, True, white_color)
        text_rect = text.get_rect()
        text_rect.topright = [WIDTH, 0]
        screen.blit(text, text_rect)


class GameOverScene(Scene):
    def update(self):
        self.playing = False

    def render(self, screen):
        font = pygame.font.SysFont('Arial', 72)
        text = font.render('GAME OVER :(', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = [WIDTH / 2, HEIGHT / 2]
        screen.blit(text, text_rect)


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


director = Director('BreakOut', (WIDTH, HEIGHT))
director.addScene('Stage1')
director.execute('Stage1')



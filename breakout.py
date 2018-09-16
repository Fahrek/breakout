import sys #para usar exit()
import pygame

WIDTH  = 640
HEIGHT = 480

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #Cargar imagen
        self.image = pygame.image.load('assets/ball.png')
        #Obtener rectangulo de la imagen
        self.rect  = self.image.get_rect()
        #Posicion inicial centrada en pantalla
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGHT/2

#Inicializando pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#Configurar título de la pantalla
pygame.display.set_caption('BreakOut')

ball = Ball()

while True:
    #Revisar todos los eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()
    pygame.display.flip()

    #Dibujar bola en pantalla
    screen.blit(ball.image, ball.rect)
    #Actualizar los elementos en pantalla
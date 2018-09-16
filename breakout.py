import sys #para usar exit()
import pygame

ANCHO = 640
ALTO  = 480

#Inicializando pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
#Configurar título de la pantalla
pygame.display.set_caption('BreakOut')


while True:
    #Revisar todos los eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()
    pygame.display.flip()
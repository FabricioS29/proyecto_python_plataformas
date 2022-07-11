#!/usr/bin/python3

"""
Alumno: Fabricio Solano Rojas
Carnet: B77447

Alumno: Miguel Zamora Torres
Carnet: B78542

Alumno: Delvin Ríos Rodríguez
Carnet: B76319

El siguiente codigo se desarrolla el codigo principal de esta version que emula
a un "Flappy Bird", se basa en la biblioteca pygame. Se determina desde la
imagen de fondo, las estructuras de choque, el objeto que se controla con cada
click del teclado.

Este archivo va de la mano con los archivos llamados caracteristicas.py y
sprites.py
"""
# Se importan las bibliotecas a utilizar y los archivos donde se encuentran
# los objetos del juego
import pygame
import sys
import time
from caracteristicas import win_Width, win_Height, framerate
from sprites import BG, Ground, Bird, Obstacle


# Se crea la clase Game, la cual va a contener todas las funciones que
# controlan el juego
class Game:
    def __init__(self):
        # Configuracion basica del juego
        # Se le da un nombre al juego, ademas de llamar las caracteristicas
        # de la ventada donde se va a jugar.
        pygame.init()
        self.display_surface = pygame.display.set_mode((win_Width, win_Height))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        self.active = True
        self.begin = False

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # Se determina la escala necesaria para el fondo, utilizando las
        # caracteristicas de la ventana.
        bg_height = pygame.image.load(('../graficos/fondo/'
                                       'fondo.png')).get_height()
        self.scale_factor = win_Height/bg_height  # Se calcula la escala
        print(self.scale_factor)

        # Se hace un llamado a las funciones del fondo y el suelo
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.bird = Bird(self.all_sprites, self.scale_factor/7)

        # Se establece el timer que controla el juego
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

        # Se establecen las caracteristicas de la fuente del juego
        self.font = pygame.font.Font(
                                    '../graficos/fuente/BD_Cartoon_Shout.ttf',
                                    30)
        self.score = 0
        self.start_offset = 0

        # Se configura el menu final del juego
        # Se determina la ubicacion de la imagen del mundo para llamarla
        self.menu_surf = pygame.image.load(
                                            '../graficos/menus/menuF.png'
                                            ).convert_alpha()
        # Se ubica el menu final en el centro de la ventana del juego
        self.menu_rect = self.menu_surf.get_rect(
                                                center=(win_Width/2,
                                                        win_Height/2)
                                                )

        # Se configura el menu inicial del juego
        # Se determina la ubicacion de la imagen del mundo para llamarla
        self.menuS_surf = pygame.image.load(
                                            '../graficos/menus/menuS.png'
                                            ).convert_alpha()
        # Se ubica el menu final en el centro de la ventana del juego
        self.menuS_rect = self.menuS_surf.get_rect(
                                                center=(win_Width/2,
                                                        win_Height/2)
                                                )

        # Se configura la musica que va a tener el juego de fondo
        self.music = pygame.mixer.Sound('../sonidos/musica.wav')
        self.music.play(loops=-1)

    # Se establece la funcion que controla las coliciones del juego
    def collisions(self):
        if pygame.sprite.spritecollide(
                                        self.bird,
                                        self.collision_sprites,
                                        False,
                                        pygame.sprite.collide_mask
                                        ) or (self.bird.rect.top <= 0):
            # Se establece que al chocar el ave con un obstaculo se determina
            # el juego
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            self.active = False
            self.bird.kill()

    # Se establece la funcion que controla el inicio del juego
    def beginning(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.sprite_type == 'obstacle':
                sprite.kill()
        self.bird.kill()

    # se determina la funcion que controla la calificacion de cada jugada
    def display_score(self):
        if self.begin is False:
            y = win_Height/10
        elif self.active:
            self.score = (pygame.time.get_ticks()-self.start_offset)//1000
            y = win_Height/10
        else:
            y = win_Height/2 + (self.menu_rect.height/1.5)
        color = (0, 0, 0)
        score_surf = self.font.render(str(self.score), True, color)
        score_rect = score_surf.get_rect(midtop=(win_Width/2, y))
        self.display_surface.blit(score_surf, score_rect)

    # Se determina la jugabilidad del juego
    def run(self):
        last_time = time.time()
        while True:
            # Se establece el tiempo delta (dt)
            dt = time.time() - last_time
            last_time = time.time()

            # Cilco para controlar los eventos del juego
            for event in pygame.event.get():
                # Se configura la forma de cerrar el juego
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Se configura el inicio del juego
                # primera tecla espacio inicia el juego
                if self.begin is False:
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_SPACE:  # tecla espacio
                            self.begin = True
                            self.bird = Bird(
                                                self.all_sprites,
                                                self.scale_factor/7
                                                )
                            self.start_offset = pygame.time.get_ticks()
                # se configura luego de la primera tecla de espacio
                else:
                    # Se configura la tecla para el salto del ave
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_SPACE:  # tecla espacio
                            # espacio para el salto
                            if self.active:
                                self.bird.jump()
                            else:
                                self.bird = Bird(
                                                    self.all_sprites,
                                                    self.scale_factor/7
                                                    )
                                self.active = True
                                self.start_offset = pygame.time.get_ticks()
                    if event.type == self.obstacle_timer and self.active:
                        Obstacle(
                                    [self.all_sprites, self.collision_sprites],
                                    self.scale_factor*1.7
                                )

            # Se establece la logica del juego
            color = (0, 0, 0)
            self.display_surface.fill(color)
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.display_score()

            # Cuando inicia mostrar menu
            if self.begin is False:
                self.beginning()
                self.display_surface.blit(self.menuS_surf, self.menuS_rect)
            # Luego de la primer tecla de espacio (inicio de juego)
            else:
                # Se verifica las colisiones
                if self.active:
                    self.collisions()
                # Cuando presenta colisiones mostrar menu final
                else:
                    self.display_surface.blit(self.menu_surf, self.menu_rect)

            pygame.display.update()
            self.clock.tick(framerate)


# Se llama al main que corra las funcones principales para correr el juego
if __name__ == '__main__':
    game = Game()
    game.run()

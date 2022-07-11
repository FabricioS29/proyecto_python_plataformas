#!/usr/bin/python3

"""
Alumno: Fabrisio Solano Rojas
Carnet: B77447

Alumno: Miguel Zamora Torres
Carnet: B78542

Alumno: Delvin Ríos Rodríguez
Carnet: B76319

En este archivo se establecen las clases que van a controlar el fondo, el
suelo, los obstaculos, el ave que controla el usuario.
"""
# Se importan las bibliotecas necesarias y los archivos de interes
import pygame
from random import choice, randint
from caracteristicas import win_Width, win_Height


# Se establece la clase que controla la imagen de fondo
class BG(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        # Se establece la direccion para encontrar la imagen
        bg_image = pygame.image.load((
                                        '../graficos/fondo/'
                                        'fondo.png'
                                    )).convert()
        # Se acondiciona la imagen para que el tamano de la ventana
        full_height = int(bg_image.get_height()*scale_factor)
        full_width = int(bg_image.get_width()*scale_factor)
        full_sized_image = pygame.transform.scale(
                                                    bg_image,
                                                    (full_width, full_height)
                                                )
        self.image = pygame.Surface((full_width*2, full_height))
        self.image.blit(full_sized_image, (0, 0))
        self.image.blit(full_sized_image, (full_width, 0))
        # Se determina la ubicacion de la imagen en la ventana
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    # Se establece el metodo que permite el movimiento de la imagen de fondo
    def update(self, dt):
        self.pos.x -= 300*dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)


# Se establece la clase que controla la imagen del suelo
class Ground(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.sprite_type = 'ground'
        # Se establece la direccion para cargar la imagen
        ground_surf = pygame.image.load((
                                            '../graficos/fondo/'
                                            'suelo.png'
                                        )).convert_alpha()
        # Se acondiciona la imagen para que coincida con la ventana de juego
        full_height1 = int(ground_surf.get_height()*scale_factor)
        full_width1 = int(ground_surf.get_width()*scale_factor)
        self.image = pygame.transform.scale(
                                                ground_surf,
                                                (full_width1, full_height1)
                                            )
        # Se determina la ubicacion donde insertar la imagen
        self.rect = self.image.get_rect(bottomleft=(0, win_Height))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # Se determina el suelo como una mascara, imagen sobrepuesta
        self.mask = pygame.mask.from_surface(self.image)

    # Se establece el metodo que permite el movimiento de la imagen del suelo
    def update(self, dt):
        self.pos.x -= 360*dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)


# Se establece la clase que controla la imagen del ave
class Bird(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        # Se acondiciona la imagen del ave
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        # Se rectifica la imagen, ubicandola siempre en el centro de la ventana
        self.rect = self.image.get_rect(midleft=(win_Width/20, win_Height/2))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        # Se establece el movimiento del ave, afectado por la gravedad
        self.gravity = 600
        self.direction = 0

        # Se determina el avel como una mascara, imagen sobrepuesta
        self.mask = pygame.mask.from_surface(self.image)

        # Se determina el sonido que va a ejecutar el ave con cada brinco
        self.jump_sound = pygame.mixer.Sound('../sonidos/salto.wav')
        self.jump_sound.set_volume(0.2)

    # Se establece la funcion que hace el efecto del movimiento de las alas
    # del ave
    def import_frames(self, scale_factor):
        self.frames = []
        # Se hace una secuencia de las imagenes que genera el movimiento
        for i in range(3):
            surf = pygame.image.load((
                                        f'../graficos/ave/ave{i}.png'
                                        )).convert_alpha()
            full_height = int(surf.get_height()*scale_factor)
            full_width = int(surf.get_width()*scale_factor)
            scaled_surface = pygame.transform.scale(
                                                    surf,
                                                    (full_width, full_height)
                                                    )
            self.frames.append(scaled_surface)

    # Se configura la gravedad que va a afectar el movimiento del ave
    def apply_gravity(self, dt):
        self.direction += self.gravity*dt
        self.pos.y += self.direction*dt
        self.rect.y = round(self.pos.y)

    # Se configura el movimiento de salto que va a tener el ave con cada
    # vez que se preciona la tecla espacio
    def jump(self):
        self.jump_sound.play()
        self.direction = -400

    # Se determina la funcion que controla la animacion del ave
    def animate(self, dt):
        self.frame_index += 10*dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    # Se determina la funcion que controla la rotacion del ave cuando cae y
    # cuando sube
    def rotate(self, dt):
        rotated_bird = pygame.transform.rotozoom(
                                                        self.image,
                                                        -self.direction*0.06,
                                                        1
                                                    )
        self.image = rotated_bird
        self.mask = pygame.mask.from_surface(self.image)

    # Se determina la funcion que hace el movimiento general del ave durante
    # el juego
    def update(self, dt):
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate(dt)


# Se establece la clase que controla los obstaculos
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.sprite_type = 'obstacle'
        # Se establece la ubicacion de los obstaculos
        orientation = choice(('up', 'down'))
        # Se determina la ubicacion de la imagen de los obstaculos
        surf = pygame.image.load((
                                f'../graficos/obstaculos/{choice((0,1))}.png'
                                )).convert_alpha()
        # Se acondicionan las imagenes para el tamano de la ventana de juego
        full_height = int(surf.get_height()*scale_factor)
        full_width = int(surf.get_width()*scale_factor)
        self.image = pygame.transform.scale(surf, (full_width, full_height))
        # Se establece la ubicacion de como van a ir apareciendo en eljuego
        x = win_Width + randint(40, 100)
        if orientation == 'up':
            y = win_Height + randint(10, 50)
            self.rect = self.image.get_rect(midbottom=(x, y))
        else:
            y = randint(-50, -10)
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midtop=(x, y))

        self.pos = pygame.math.Vector2(self.rect.topleft)

        # Se determina el ave como una mascara, imagen sobrepuesta
        self.mask = pygame.mask.from_surface(self.image)

    # Se determina la funcion que controla el movimiento de los obstaculos
    def update(self, dt):
        self.pos.x -= 400*dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -100:
            self.kill()

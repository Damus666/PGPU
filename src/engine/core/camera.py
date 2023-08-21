from .window import Window
import pygame

class Camera:
    position:pygame.Vector2= pygame.Vector2()

    @classmethod
    def screen_to_world(cls, position):
        return pygame.Vector2(position)-Window.center-cls.position
    
    @classmethod
    def world_to_screen(cls, position):
        return pygame.Vector2(position)+Window.center+cls.position
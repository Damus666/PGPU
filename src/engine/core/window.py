import pygame._sdl2 as pgsdl
import pygame

class Window:
    window: pgsdl.Window = None
    renderer: pgsdl.Renderer = None
    bounds: pygame.Rect = None
    center: pygame.Vector2 = None

    @classmethod
    def _init(cls, window:pgsdl.Window, accelerated:bool=True):
        cls.window = window
        cls.renderer = pgsdl.Renderer(cls.window, accelerated=accelerated)
        cls.bounds = pygame.Rect(0,0,window.size[0], window.size[1])
        cls.center = pygame.Vector2(cls.bounds.center)
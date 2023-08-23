from .window import Window
import pygame
from ..utils import Vectorizable


class Camera:
    position: pygame.Vector2 = pygame.Vector2()

    @classmethod
    def screen_to_world(
        cls,
        position: Vectorizable,
    ) -> pygame.Vector2:
        return position - Window.center - cls.position

    @classmethod
    def world_to_screen(
        cls,
        position: Vectorizable,
    ) -> pygame.Vector2:
        return position + Window.center + cls.position
    
    @classmethod
    def project_point(cls, point:Vectorizable):
        return point- cls.position+Window.center

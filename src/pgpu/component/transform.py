import pygame


class Transform:
    def __init__(
        self,
        position: pygame.Vector2 = (0,0),
        scale: pygame.Vector2 = (1,1),
        rotation: float = 0,
        flipx: bool = False,
        flipy: bool = False,
    ):
        self.position: pygame.Vector2 = pygame.Vector2(position)
        self.scale: pygame.Vector2 = pygame.Vector2(scale)
        self.rotation: float = float(rotation)
        self.flipx: bool = bool(flipx)
        self.flipy: bool = bool(flipy)

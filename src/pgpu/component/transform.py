import pygame


class Transform:
    def __init__(
        self,
        position: pygame.Vector2 = None,
        scale: pygame.Vector2 = None,
        rotation: float = None,
        flipx: bool = None,
        flipy: bool = None,
    ):
        self.position: pygame.Vector2 = (
            pygame.Vector2() if position is None else pygame.Vector2(position)
        )
        self.scale: pygame.Vector2 = (
            pygame.Vector2(1, 1) if scale is None else pygame.Vector2(scale)
        )
        self.rotation: float = 0 if rotation is None else float(rotation)
        self.flipx: bool = False if flipx is None else bool(flipx)
        self.flipy: bool = False if flipy is None else bool(flipy)

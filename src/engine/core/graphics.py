import pygame, math, random
import pygame._sdl2 as pgsdl
from .window import Window

class Graphics:
    @staticmethod
    def empty_texture(size=(100,100), color="black"):
        surf = pygame.Surface(size)
        surf.fill(color)
        tex = pgsdl.Texture.from_surface(Window.renderer, surf)
        return tex
    
    @staticmethod
    def from_surface(surface: pygame,Surface):
        return pgsdl.Texture.from_surface(Window.renderer, surface)
    
    @staticmethod
    def random_color():
        return pygame.Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    
    @staticmethod
    def radial_surface(surface:pygame.Surface, erase_angle):
        erase_angle -= 180
        surface = surface.copy()
        w,h = surface.get_size()
        cx, cy = w//2, h//2
        center = pygame.Vector2(cx,cy)
        for x in range(w):
            for y in range(h):
                if surface.get_at((x,y)).a == 0: continue
                direction = pygame.Vector2(x,y)-center
                if math.degrees(math.atan2(direction.x, -direction.y)) < erase_angle: surface.set_at((x,y), (0,0,0,0))
        return surface
    
    @staticmethod
    def surface_outline(
        surface: pygame.Surface,
        radius: int,
        color: pygame.Color | list[int] | tuple[int, ...] = (0, 0, 0, 255),
        rounded: bool = False,
        border_inflate_x: int = 0,
        border_inflate_y: int = 0,
        mask_threshold=127,
        sharpness_passes: int = 4,
    ) -> pygame.Surface:
        surf_size = surface.get_size()
        backdrop_surf_size = (
            surf_size[0] + radius + border_inflate_x,
            surf_size[1] + radius + border_inflate_y,
        )

        silhouette = pygame.mask.from_surface(surface, threshold=mask_threshold).to_surface(
            setcolor=color, unsetcolor=(0, 0, 0, 0)
        )
        backdrop = pygame.Surface((backdrop_surf_size), pygame.SRCALPHA)
        blit_topleft = (
            backdrop_surf_size[0] / 2 - surf_size[0] / 2,
            backdrop_surf_size[1] / 2 - surf_size[1] / 2,
        )
        backdrop.blit(silhouette, blit_topleft)
        backdrop_blurred = (
            pygame.transform.gaussian_blur(backdrop, radius=radius)
            if rounded
            else pygame.transform.box_blur(backdrop, radius=radius)
        )
        for _ in range(sharpness_passes):
            backdrop_blurred.blit(
                backdrop_blurred, (0, 0), special_flags=pygame.BLEND_RGBA_ADD
            )

        backdrop_blurred.blit(surface, blit_topleft)
        return backdrop_blurred
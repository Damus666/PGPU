import pygame, math, random, os
import pygame._sdl2 as pgsdl
from .window import Window
from ..utils import ColorValue


class Asset:
    def __init__(
        self, surface: pygame.Surface, texture: pgsdl.Texture = None, name: str = None
    ):
        self.name: str = name if name is not None else "Unnamed Asset"
        self.surface: pygame.Surface = surface
        self.texture: pgsdl.Texture = (
            texture
            if texture is not None
            else pgsdl.Texture.from_surface(Window.renderer, self.surface)
        )


class AssetList:
    def __init__(self, assets: list[Asset] = None):
        self.assets: list[Asset] = [] if assets is None else assets.copy()

    def add(
        self, surface: pygame.Surface, texture: pgsdl.Texture = None, name: str = None
    ) -> Asset:
        asset = Asset(surface, texture, name)
        self.assets.append(asset)
        return asset

    def add_asset(self, asset: Asset):
        self.assets.append(asset)

    def textures(self) -> list[pgsdl.Texture]:
        return [asset.texture for asset in self.assets]

    def surfaces(self) -> list[pygame.Surface]:
        return [asset.surface for asset in self.assets]


class AssetDict:
    def __init__(self, assets: list[Asset] = None):
        self.assets: dict[str, Asset] = {}
        assets = assets if assets is not None else []
        for asset in assets:
            self.assets[asset.name] = asset

    def add(
        self, surface: pygame.Surface, texture: pgsdl.Texture = None, name: str = None
    ) -> Asset:
        asset = Asset(surface, texture, name)
        self.assets[asset.name] = asset
        return asset

    def add_asset(self, asset: Asset):
        self.assets[asset.name] = asset

    def textures(self) -> list[pgsdl.Texture]:
        return [asset.texture for asset in self.assets.values()]

    def surfaces(self) -> list[pygame.Surface]:
        return [asset.surface for asset in self.assets.values()]


def load(path: str, scale_factor: float | tuple[float, float] = 1) -> pgsdl.Texture:
    return pgsdl.Texture.from_surface(
        Window.renderer,
        pygame.transform.scale_by(pygame.image.load(path), scale_factor),
    )


def load_cached(
    path: str, scale_factor: float | tuple[float, float] = 1
) -> list[pgsdl.Texture, pygame.Surface]:
    surf = pygame.transform.scale_by(pygame.image.load(path), scale_factor)
    return [pgsdl.Texture.from_surface(Window.renderer, surf), surf]


def load_asset(
    path: str, scale_factor: float | tuple[float, float], name: str = None
) -> Asset:
    return Asset(
        pygame.transform.scale_by(pygame.image.load(path), scale_factor), None, name
    )


def load_list(
    folder_path: str, scale_factor: float | tuple[float, float] = 1
) -> list[pgsdl.Texture]:
    texs = []
    for image in os.listdir(folder_path):
        if "." in image:
            try:
                tex = pgsdl.Texture.from_surface(
                    Window.renderer,
                    pygame.transform.scale_by(
                        pygame.image.load(folder_path + "/" + image), scale_factor
                    ),
                )
                texs.append(tex)
            except:
                pass
    return texs


def load_cached_list(
    folder_path: str, scale_factor: float | tuple[float, float] = 1
) -> list[list[pgsdl.Texture, pygame.Surface]]:
    texs = []
    for image in os.listdir(folder_path):
        if "." in image:
            try:
                surf = pygame.transform.scale_by(
                    pygame.image.load(folder_path + "/" + image), scale_factor
                )
                tex = pgsdl.Texture.from_surface(Window.renderer, surf)
                texs.append([tex, surf])
            except:
                pass
    return texs


def load_asset_list(
    folder_path: str, scale_factor: float | tuple[float, float] = 1
) -> AssetList:
    asset_list = AssetList()
    for image in os.listdir(folder_path):
        if "." in image:
            try:
                asset_list.add(
                    Window.renderer,
                    pygame.transform.scale_by(
                        pygame.image.load(folder_path + "/" + image), scale_factor
                    ),
                    None,
                    image.split(".")[0],
                )
            except:
                pass
    return asset_list


def load_dict(
    folder_path: str, scale_factor: float | tuple[float, float] = 1
) -> dict[str, pgsdl.Texture]:
    texs = {}
    for image in os.listdir(folder_path):
        if "." in image:
            try:
                tex = pgsdl.Texture.from_surface(
                    Window.renderer,
                    pygame.transform.scale_by(
                        pygame.image.load(folder_path + "/" + image), scale_factor
                    ),
                )
                texs[image.split(".")[0]] = tex
            except:
                pass
    return texs


def load_cached_dict(
    folder_path: str, scale_factor: float | tuple[float, float] = 1
) -> dict[str, list[pgsdl.Texture, pygame.Surface]]:
    texs = {}
    for image in os.listdir(folder_path):
        if "." in image:
            try:
                surf = pygame.transform.scale_by(
                    pygame.image.load(folder_path + "/" + image), scale_factor
                )
                tex = pgsdl.Texture.from_surface(Window.renderer, surf)
                texs[image.split(".")[0]] = [tex, surf]
            except:
                pass
    return texs


def load_asset_dict(
    folder_path: str, scale_factor: float | tuple[float, float] = 1
) -> AssetDict:
    asset_dict = AssetDict()
    for image in os.listdir(folder_path):
        if "." in image:
            try:
                AssetDict.add(
                    pygame.transform.scale_by(
                        pygame.image.load(folder_path + "/" + image), scale_factor
                    ),
                    None,
                    image.split(".")[0],
                )
            except:
                pass
    return asset_dict

def box_texture(
    size: tuple[int, int] = (100, 100), color: str = "black"
) -> pgsdl.Texture:
    surf = pygame.Surface(size)
    surf.fill(color)
    tex = pgsdl.Texture.from_surface(Window.renderer, surf)
    return tex


def circle_texture(radius: float, color, width: int = 0):
    surf = pygame.Surface((int(radius * 2), int(radius * 2)), pygame.SRCALPHA)
    surf.fill(0)
    pygame.draw.circle(surf, color, (radius, radius), radius, width)
    return pgsdl.Texture.from_surface(Window.renderer, surf)


def from_surface(surface: pygame.Surface) -> pgsdl.Texture:
    return pgsdl.Texture.from_surface(Window.renderer, surface)


def font_texture(
    font: pygame.Font,
    text: str | bytes | None,
    antialas: bool,
    color: ColorValue,
    bgcolor: ColorValue = None,
    wraplength: int = 0,
):
    return pgsdl.Texture.from_surface(
        Window.renderer, font.render(text, antialas, color, bgcolor, wraplength)
    )


def random_color(rand_alpha: bool = False) -> pygame.Color:
    return pygame.Color(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255) if rand_alpha else 255,
    )


def radial_surface(surface: pygame.Surface, erase_angle: float) -> pygame.Surface:
    erase_angle -= 180
    surface = surface.copy()
    w, h = surface.get_size()
    cx, cy = w // 2, h // 2
    center = pygame.Vector2(cx, cy)
    for x in range(w):
        for y in range(h):
            if surface.get_at((x, y)).a == 0:
                continue
            if (pygame.Vector2(x, y) - center).as_polar()[1] < erase_angle:
                surface.set_at((x, y), (0, 0, 0, 0))
    return surface


def surface_outline(
    surface: pygame.Surface,
    radius: int,
    color: pygame.Color | list[int] | tuple[int, ...] = (0, 0, 0, 255),
    rounded: bool = False,
    border_inflate_x: int = 0,
    border_inflate_y: int = 0,
    mask_threshold: int = 127,
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

import random
import pygame
from typing import Optional, Iterable


def rgb_to_hex(rgb_color: tuple[int, int, int]) -> str:
    return "%02x%02x%02x" % rgb_color


def rgba_to_hex(rgba_color: tuple[int, int, int]) -> str:
    return "%02x%02x%02x%02x" % rgba_color


def hex_to_rgb(HEXColor: str) -> tuple[int, ...]:
    value = HEXColor.lstrip("#")
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


def to_tuple(color: pygame.Color) -> tuple[int, int, int, int]:
    return (color.r, color.g, color.b, color.a)


def to_range_01(
    color_range_0255: Iterable[int], has_alpha: bool = True
) -> tuple[float, float, float] | tuple[float, float, float, float]:
    if not has_alpha:
        return (
            color_range_0255[0] / 255,
            color_range_0255[1] / 255,
            color_range_0255[2] / 255,
        )
    return (
        color_range_0255[0] / 255,
        color_range_0255[1] / 255,
        color_range_0255[2] / 255,
        color_range_0255[3] / 255,
    )


def to_range_0255(
    color_range_01: Iterable[float], has_alpha: bool = True
) -> tuple[int, int, int] | tuple[int, int, int, int]:
    if not has_alpha:
        return (
            int(color_range_01[0] * 255),
            int(color_range_01[1] * 255),
            int(color_range_01[2] * 255),
        )
    return (
        int(color_range_01[0] * 255),
        int(color_range_01[1] * 255),
        int(color_range_01[2] * 255),
        int(color_range_01[3] * 255),
    )


def clamp_value(value: float) -> int:
    return pygame.math.clamp(int(value), 0, 255)


def clamp(color: Iterable[float]) -> tuple[int, ...]:
    return tuple([pygame.math.clamp(int(value), 0, 1) for value in color])


def is_valid(color: Iterable):
    return all(
        [isinstance(value, int) and value >= 0 and value <= 255 for value in color]
    )


def random_rgb() -> pygame.Color:
    return pygame.Color(
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    )


def random_rgba() -> pygame.Color:
    return pygame.Color(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


def random_rgb_tuple() -> tuple[int, int, int]:
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def random_rgba_tuple() -> tuple[int, int, int, int]:
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


def random_name() -> str:
    return random.choice(list(COLORS.keys()))


def random_color() -> pygame.Color:
    return random.choice(list(COLORS.values()))


def color_names() -> list[str]:
    return list(COLORS.keys())


def colors() -> list[pygame.Color]:
    return list(COLORS.values())


def exists(name: str) -> bool:
    return name in COLORS


class Colors:
    maroon: pygame.Color = pygame.Color(128, 0, 0)
    dark_red: pygame.Color = pygame.Color(139, 0, 0)
    brown: pygame.Color = pygame.Color(165, 42, 42)
    firebrick: pygame.Color = pygame.Color(178, 34, 34)
    crimson: pygame.Color = pygame.Color(220, 20, 60)
    red: pygame.Color = pygame.Color(255, 0, 0)
    tomato: pygame.Color = pygame.Color(255, 99, 71)
    coral: pygame.Color = pygame.Color(255, 127, 80)
    indian_red: pygame.Color = pygame.Color(205, 92, 92)
    light_coral: pygame.Color = pygame.Color(240, 128, 128)
    dark_salmon: pygame.Color = pygame.Color(233, 150, 122)
    salmon: pygame.Color = pygame.Color(250, 128, 114)
    light_salmon: pygame.Color = pygame.Color(255, 160, 122)
    orange_red: pygame.Color = pygame.Color(255, 69, 0)
    dark_orange: pygame.Color = pygame.Color(255, 140, 0)
    orange: pygame.Color = pygame.Color(255, 165, 0)
    gold: pygame.Color = pygame.Color(255, 215, 0)
    dark_golden_rod: pygame.Color = pygame.Color(184, 134, 11)
    golden_rod: pygame.Color = pygame.Color(218, 165, 32)
    pale_golden_rod: pygame.Color = pygame.Color(238, 232, 170)
    dark_khaki: pygame.Color = pygame.Color(189, 183, 107)
    khaki: pygame.Color = pygame.Color(240, 230, 140)
    olive: pygame.Color = pygame.Color(128, 128, 0)
    yellow: pygame.Color = pygame.Color(255, 255, 0)
    yellow_green: pygame.Color = pygame.Color(154, 205, 50)
    dark_olive_green: pygame.Color = pygame.Color(85, 107, 47)
    olive_drab: pygame.Color = pygame.Color(107, 142, 35)
    lawn_green: pygame.Color = pygame.Color(124, 252, 0)
    chartreuse: pygame.Color = pygame.Color(127, 255, 0)
    green_yellow: pygame.Color = pygame.Color(173, 255, 47)
    dark_green: pygame.Color = pygame.Color(0, 100, 0)
    green: pygame.Color = pygame.Color(0, 128, 0)
    forest_green: pygame.Color = pygame.Color(34, 139, 34)
    lime: pygame.Color = pygame.Color(0, 255, 0)
    lime_green: pygame.Color = pygame.Color(50, 205, 50)
    light_green: pygame.Color = pygame.Color(144, 238, 144)
    pale_green: pygame.Color = pygame.Color(152, 251, 152)
    dark_sea_green: pygame.Color = pygame.Color(143, 188, 143)
    medium_spring_green: pygame.Color = pygame.Color(0, 250, 154)
    spring_green: pygame.Color = pygame.Color(0, 255, 127)
    sea_green: pygame.Color = pygame.Color(46, 139, 87)
    medium_aqua_marine: pygame.Color = pygame.Color(102, 205, 170)
    medium_sea_green: pygame.Color = pygame.Color(60, 179, 113)
    light_sea_green: pygame.Color = pygame.Color(32, 178, 170)
    dark_slate_gray: pygame.Color = pygame.Color(47, 79, 79)
    teal: pygame.Color = pygame.Color(0, 128, 128)
    dark_cyan: pygame.Color = pygame.Color(0, 139, 139)
    aqua: pygame.Color = pygame.Color(0, 255, 255)
    cyan: pygame.Color = pygame.Color(0, 255, 255)
    light_cyan: pygame.Color = pygame.Color(224, 255, 255)
    dark_turquoise: pygame.Color = pygame.Color(0, 206, 209)
    turquoise: pygame.Color = pygame.Color(64, 224, 208)
    medium_turquoise: pygame.Color = pygame.Color(72, 209, 204)
    pale_turquoise: pygame.Color = pygame.Color(175, 238, 238)
    aqua_marine: pygame.Color = pygame.Color(127, 255, 212)
    powder_blue: pygame.Color = pygame.Color(176, 224, 230)
    cadet_blue: pygame.Color = pygame.Color(95, 158, 160)
    steel_blue: pygame.Color = pygame.Color(70, 130, 180)
    corn_flower_blue: pygame.Color = pygame.Color(100, 149, 237)
    deep_sky_blue: pygame.Color = pygame.Color(0, 191, 255)
    dodger_blue: pygame.Color = pygame.Color(30, 144, 255)
    light_blue: pygame.Color = pygame.Color(173, 216, 230)
    sky_blue: pygame.Color = pygame.Color(135, 206, 235)
    light_sky_blue: pygame.Color = pygame.Color(135, 206, 250)
    midnight_blue: pygame.Color = pygame.Color(25, 25, 112)
    navy: pygame.Color = pygame.Color(0, 0, 128)
    dark_blue: pygame.Color = pygame.Color(0, 0, 139)
    medium_blue: pygame.Color = pygame.Color(0, 0, 205)
    blue: pygame.Color = pygame.Color(0, 0, 255)
    royal_blue: pygame.Color = pygame.Color(65, 105, 225)
    blue_violet: pygame.Color = pygame.Color(138, 43, 226)
    indigo: pygame.Color = pygame.Color(75, 0, 130)
    dark_slate_blue: pygame.Color = pygame.Color(72, 61, 139)
    slate_blue: pygame.Color = pygame.Color(106, 90, 205)
    medium_slate_blue: pygame.Color = pygame.Color(123, 104, 238)
    medium_purple: pygame.Color = pygame.Color(147, 112, 219)
    dark_magenta: pygame.Color = pygame.Color(139, 0, 139)
    dark_violet: pygame.Color = pygame.Color(148, 0, 211)
    dark_orchid: pygame.Color = pygame.Color(153, 50, 204)
    medium_orchid: pygame.Color = pygame.Color(186, 85, 211)
    purple: pygame.Color = pygame.Color(128, 0, 128)
    thistle: pygame.Color = pygame.Color(216, 191, 216)
    plum: pygame.Color = pygame.Color(221, 160, 221)
    violet: pygame.Color = pygame.Color(238, 130, 238)
    magenta: pygame.Color = pygame.Color(255, 0, 255)
    fuchsia: pygame.Color = pygame.Color(255, 0, 255)
    orchid: pygame.Color = pygame.Color(218, 112, 214)
    medium_violet_red: pygame.Color = pygame.Color(199, 21, 133)
    pale_violet_red: pygame.Color = pygame.Color(219, 112, 147)
    deep_pink: pygame.Color = pygame.Color(255, 20, 147)
    hot_pink: pygame.Color = pygame.Color(255, 105, 180)
    light_pink: pygame.Color = pygame.Color(255, 182, 193)
    pink: pygame.Color = pygame.Color(255, 192, 203)
    antique_white: pygame.Color = pygame.Color(250, 235, 215)
    beige: pygame.Color = pygame.Color(245, 245, 220)
    bisque: pygame.Color = pygame.Color(255, 228, 196)
    blanched_almond: pygame.Color = pygame.Color(255, 235, 205)
    wheat: pygame.Color = pygame.Color(245, 222, 179)
    corn_silk: pygame.Color = pygame.Color(255, 248, 220)
    lemon_chiffon: pygame.Color = pygame.Color(255, 250, 205)
    light_golden_rod_yellow: pygame.Color = pygame.Color(250, 250, 210)
    light_yellow: pygame.Color = pygame.Color(255, 255, 224)
    saddle_brown: pygame.Color = pygame.Color(139, 69, 19)
    sienna: pygame.Color = pygame.Color(160, 82, 45)
    chocolate: pygame.Color = pygame.Color(210, 105, 30)
    peru: pygame.Color = pygame.Color(205, 133, 63)
    sandy_brown: pygame.Color = pygame.Color(244, 164, 96)
    burly_wood: pygame.Color = pygame.Color(222, 184, 135)
    tan: pygame.Color = pygame.Color(210, 180, 140)
    rosy_brown: pygame.Color = pygame.Color(188, 143, 143)
    moccasin: pygame.Color = pygame.Color(255, 228, 181)
    navajo_white: pygame.Color = pygame.Color(255, 222, 173)
    peach_puff: pygame.Color = pygame.Color(255, 218, 185)
    misty_rose: pygame.Color = pygame.Color(255, 228, 225)
    lavender_blush: pygame.Color = pygame.Color(255, 240, 245)
    linen: pygame.Color = pygame.Color(250, 240, 230)
    old_lace: pygame.Color = pygame.Color(253, 245, 230)
    papaya_whip: pygame.Color = pygame.Color(255, 239, 213)
    sea_shell: pygame.Color = pygame.Color(255, 245, 238)
    mint_cream: pygame.Color = pygame.Color(245, 255, 250)
    slate_gray: pygame.Color = pygame.Color(112, 128, 144)
    light_slate_gray: pygame.Color = pygame.Color(119, 136, 153)
    light_steel_blue: pygame.Color = pygame.Color(176, 196, 222)
    lavender: pygame.Color = pygame.Color(230, 230, 250)
    floral_white: pygame.Color = pygame.Color(255, 250, 240)
    alice_blue: pygame.Color = pygame.Color(240, 248, 255)
    ghost_white: pygame.Color = pygame.Color(248, 248, 255)
    honeydew: pygame.Color = pygame.Color(240, 255, 240)
    ivory: pygame.Color = pygame.Color(255, 255, 240)
    azure: pygame.Color = pygame.Color(240, 255, 255)
    snow: pygame.Color = pygame.Color(255, 250, 250)
    black: pygame.Color = pygame.Color(0, 0, 0)
    dim_gray: pygame.Color = pygame.Color(105, 105, 105)
    dim_grey: pygame.Color = pygame.Color(105, 105, 105)
    grey: pygame.Color = pygame.Color(128, 128, 128)
    gray: pygame.Color = pygame.Color(128, 128, 128)
    dark_gray: pygame.Color = pygame.Color(169, 169, 169)
    dark_grey: pygame.Color = pygame.Color(169, 169, 169)
    silver: pygame.Color = pygame.Color(192, 192, 192)
    light_gray: pygame.Color = pygame.Color(211, 211, 211)
    light_grey: pygame.Color = pygame.Color(211, 211, 211)
    gainsboro: pygame.Color = pygame.Color(220, 220, 220)
    white_smoke: pygame.Color = pygame.Color(245, 245, 245)
    white: pygame.Color = pygame.Color(255, 255, 255)


COLORS = {
    "maroon": pygame.Color(128, 0, 0),
    "dark red": pygame.Color(139, 0, 0),
    "brown": pygame.Color(165, 42, 42),
    "firebrick": pygame.Color(178, 34, 34),
    "crimson": pygame.Color(220, 20, 60),
    "red": pygame.Color(255, 0, 0),
    "tomato": pygame.Color(255, 99, 71),
    "coral": pygame.Color(255, 127, 80),
    "indian red": pygame.Color(205, 92, 92),
    "light coral": pygame.Color(240, 128, 128),
    "dark salmon": pygame.Color(233, 150, 122),
    "salmon": pygame.Color(250, 128, 114),
    "light salmon": pygame.Color(255, 160, 122),
    "orange red": pygame.Color(255, 69, 0),
    "dark orange": pygame.Color(255, 140, 0),
    "orange": pygame.Color(255, 165, 0),
    "gold": pygame.Color(255, 215, 0),
    "dark golden rod": pygame.Color(184, 134, 11),
    "golden rod": pygame.Color(218, 165, 32),
    "pale golden rod": pygame.Color(238, 232, 170),
    "dark khaki": pygame.Color(189, 183, 107),
    "khaki": pygame.Color(240, 230, 140),
    "olive": pygame.Color(128, 128, 0),
    "yellow": pygame.Color(255, 255, 0),
    "yellow green": pygame.Color(154, 205, 50),
    "dark olive green": pygame.Color(85, 107, 47),
    "olive drab": pygame.Color(107, 142, 35),
    "lawn green": pygame.Color(124, 252, 0),
    "chartreuse": pygame.Color(127, 255, 0),
    "green yellow": pygame.Color(173, 255, 47),
    "dark green": pygame.Color(0, 100, 0),
    "green": pygame.Color(0, 128, 0),
    "forest green": pygame.Color(34, 139, 34),
    "lime": pygame.Color(0, 255, 0),
    "lime green": pygame.Color(50, 205, 50),
    "light green": pygame.Color(144, 238, 144),
    "pale green": pygame.Color(152, 251, 152),
    "dark sea green": pygame.Color(143, 188, 143),
    "medium spring green": pygame.Color(0, 250, 154),
    "spring green": pygame.Color(0, 255, 127),
    "sea green": pygame.Color(46, 139, 87),
    "medium aqua marine": pygame.Color(102, 205, 170),
    "medium sea green": pygame.Color(60, 179, 113),
    "light sea green": pygame.Color(32, 178, 170),
    "dark slate gray": pygame.Color(47, 79, 79),
    "teal": pygame.Color(0, 128, 128),
    "dark cyan": pygame.Color(0, 139, 139),
    "aqua": pygame.Color(0, 255, 255),
    "cyan": pygame.Color(0, 255, 255),
    "light cyan": pygame.Color(224, 255, 255),
    "dark turquoise": pygame.Color(0, 206, 209),
    "turquoise": pygame.Color(64, 224, 208),
    "medium turquoise": pygame.Color(72, 209, 204),
    "pale turquoise": pygame.Color(175, 238, 238),
    "aqua marine": pygame.Color(127, 255, 212),
    "powder blue": pygame.Color(176, 224, 230),
    "cadet blue": pygame.Color(95, 158, 160),
    "steel blue": pygame.Color(70, 130, 180),
    "corn flower blue": pygame.Color(100, 149, 237),
    "deep sky blue": pygame.Color(0, 191, 255),
    "dodger blue": pygame.Color(30, 144, 255),
    "light blue": pygame.Color(173, 216, 230),
    "sky blue": pygame.Color(135, 206, 235),
    "light sky blue": pygame.Color(135, 206, 250),
    "midnight blue": pygame.Color(25, 25, 112),
    "navy": pygame.Color(0, 0, 128),
    "dark blue": pygame.Color(0, 0, 139),
    "medium blue": pygame.Color(0, 0, 205),
    "blue": pygame.Color(0, 0, 255),
    "royal blue": pygame.Color(65, 105, 225),
    "blue violet": pygame.Color(138, 43, 226),
    "indigo": pygame.Color(75, 0, 130),
    "dark slate blue": pygame.Color(72, 61, 139),
    "slate blue": pygame.Color(106, 90, 205),
    "medium slate blue": pygame.Color(123, 104, 238),
    "medium purple": pygame.Color(147, 112, 219),
    "dark magenta": pygame.Color(139, 0, 139),
    "dark violet": pygame.Color(148, 0, 211),
    "dark orchid": pygame.Color(153, 50, 204),
    "medium orchid": pygame.Color(186, 85, 211),
    "purple": pygame.Color(128, 0, 128),
    "thistle": pygame.Color(216, 191, 216),
    "plum": pygame.Color(221, 160, 221),
    "violet": pygame.Color(238, 130, 238),
    "magenta": pygame.Color(255, 0, 255),
    "fuchsia": pygame.Color(255, 0, 255),
    "orchid": pygame.Color(218, 112, 214),
    "medium violet red": pygame.Color(199, 21, 133),
    "pale violet red": pygame.Color(219, 112, 147),
    "deep pink": pygame.Color(255, 20, 147),
    "hot pink": pygame.Color(255, 105, 180),
    "light pink": pygame.Color(255, 182, 193),
    "pink": pygame.Color(255, 192, 203),
    "antique white": pygame.Color(250, 235, 215),
    "beige": pygame.Color(245, 245, 220),
    "bisque": pygame.Color(255, 228, 196),
    "blanched almond": pygame.Color(255, 235, 205),
    "wheat": pygame.Color(245, 222, 179),
    "corn silk": pygame.Color(255, 248, 220),
    "lemon chiffon": pygame.Color(255, 250, 205),
    "light golden rod yellow": pygame.Color(250, 250, 210),
    "light yellow": pygame.Color(255, 255, 224),
    "saddle brown": pygame.Color(139, 69, 19),
    "sienna": pygame.Color(160, 82, 45),
    "chocolate": pygame.Color(210, 105, 30),
    "peru": pygame.Color(205, 133, 63),
    "sandy brown": pygame.Color(244, 164, 96),
    "burly wood": pygame.Color(222, 184, 135),
    "tan": pygame.Color(210, 180, 140),
    "rosy brown": pygame.Color(188, 143, 143),
    "moccasin": pygame.Color(255, 228, 181),
    "navajo white": pygame.Color(255, 222, 173),
    "peach puff": pygame.Color(255, 218, 185),
    "misty rose": pygame.Color(255, 228, 225),
    "lavender blush": pygame.Color(255, 240, 245),
    "linen": pygame.Color(250, 240, 230),
    "old lace": pygame.Color(253, 245, 230),
    "papaya whip": pygame.Color(255, 239, 213),
    "sea shell": pygame.Color(255, 245, 238),
    "mint cream": pygame.Color(245, 255, 250),
    "slate gray": pygame.Color(112, 128, 144),
    "light slate gray": pygame.Color(119, 136, 153),
    "light steel blue": pygame.Color(176, 196, 222),
    "lavender": pygame.Color(230, 230, 250),
    "floral white": pygame.Color(255, 250, 240),
    "alice blue": pygame.Color(240, 248, 255),
    "ghost white": pygame.Color(248, 248, 255),
    "honeydew": pygame.Color(240, 255, 240),
    "ivory": pygame.Color(255, 255, 240),
    "azure": pygame.Color(240, 255, 255),
    "snow": pygame.Color(255, 250, 250),
    "black": pygame.Color(0, 0, 0),
    "dim gray": pygame.Color(105, 105, 105),
    "dim grey": pygame.Color(105, 105, 105),
    "grey": pygame.Color(128, 128, 128),
    "gray": pygame.Color(128, 128, 128),
    "dark gray": pygame.Color(169, 169, 169),
    "dark grey": pygame.Color(169, 169, 169),
    "silver": pygame.Color(192, 192, 192),
    "light gray": pygame.Color(211, 211, 211),
    "light grey": pygame.Color(211, 211, 211),
    "gainsboro": pygame.Color(220, 220, 220),
    "white smoke": pygame.Color(245, 245, 245),
    "white": pygame.Color(255, 255, 255),
}

COLOR_COMBINATIONS = 256**3

import math, pygame
from ..utils import Vectorizable


def signof(x: float) -> int:
    return 1 if x > 0 else -1 if x < 0 else 0


def lerp(start: float, end: float, t: float) -> float:
    return (end - start) * t + start


def angle_to_vec(angle: float) -> pygame.Vector2:
    return pygame.Vector2(math.cos(math.radians(angle)), -math.sin(math.radians(angle)))


def inside_range(number: float, range_start: float, range_end: float) -> bool:
    return number >= min(range_start, range_end) and number <= max(
        range_start, range_end
    )


def point_circle(point: Vectorizable, center: Vectorizable, radius: float) -> bool:
    return (pygame.Vector2(point) - pygame.Vector2(center)).length() <= radius


def rect_circle(rect: pygame.Rect, center: Vectorizable, radius: float) -> bool:
    center = pygame.Vector2(center)
    return (
        pygame.Vector2(
            center.x - max(rect.left, min(center.x, rect.right)),
            center.y - max(rect.top, min(center.y, rect.bottom)),
        ).length()
        <= radius
    )

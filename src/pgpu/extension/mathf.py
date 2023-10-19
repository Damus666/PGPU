import math, pygame
from ..core.time import Time
from ..utils import Vectorizable


def lerp(start: float, end: float, t: float) -> float:
    return (end - start) * t + start


def ease_in_lerp(start: float, end: float, t: float) -> float:
    return start + (end - start) * t**2


def ease_out_lerp(start: float, end: float, t: float) -> float:
    return start + (end - start) * (1 - (1 - t) ** 2)


def smoothstep_lerp(start: float, end: float, t: float) -> float:
    t = t * t * (3 - 2 * t)
    return start + (end - start) * t


def smootherstep_lerp(start: float, end: float, t: float) -> float:
    t = t * t * t * (t * (t * 6 - 15) + 10)
    return start + (end - start) * t


def ease_in_out_lerp(start: float, end: float, t: float) -> float:
    t = t * t * (3 - 2 * t)
    return start + (end - start) * t


def quadratic_in_lerp(start: float, end: float, t: float) -> float:
    return start + (end - start) * t * t


def quadratic_out_lerp(start: float, end: float, t: float) -> float:
    return start + (end - start) * t * (2 - t)


def cubic_in_lerp(start: float, end: float, t: float) -> float:
    return start + (end - start) * t * t * t


def cubic_out_lerp(start: float, end: float, t: float) -> float:
    t -= 1
    return start + (end - start) * (t * t * t + 1)


def signof(x: float) -> int:
    return 1 if x > 0 else -1 if x < 0 else 0


def oscillate(
    start: float = 0, frequency: float = 1, scale: float = 1, func=math.sin
) -> float:
    return start + func(Time.ticks * frequency) * scale


def angle_to_vector(angle: float) -> pygame.Vector2:
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

def line_rect(start: Vectorizable, end: Vectorizable, rect: pygame.Rect) -> bool:
    start, end = pygame.Vector2(start), pygame.Vector2(end)
    min_x, max_x, min_y, max_y = rect.left, rect.right, rect.top, rect.bottom
    
    if start.x < min_x and end.x < min_x:
        return False
    if start.x > max_x and end.x > max_x:
        return False
    if start.y < min_y and end.y < min_y:
        return False
    if start.y > max_y and end.y > max_y:
        return False
    
    direction = end - start
    
    t_values = []
    if direction.x != 0:
        t_left = (min_x - start.x) / direction.x
        t_right = (max_x - start.x) / direction.x
        t_values.extend([t_left, t_right])
    if direction.y != 0:
        t_top = (min_y - start.y) / direction.y
        t_bottom = (max_y - start.y) / direction.y
        t_values.extend([t_top, t_bottom])
    
    for t in t_values:
        if 0 <= t <= 1:
            return True
    
    return False
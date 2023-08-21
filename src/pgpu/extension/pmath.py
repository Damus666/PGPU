import math, pygame


def signof(x: float) -> int:
    return 1 if x > 0 else -1 if x < 0 else 0


def lerp(start: float, end: float, t: float) -> float:
    return (end - start) * t + start


def angle_to_vec(angle: float) -> pygame.Vector2:
    return pygame.Vector2(math.cos(math.radians(angle)), -math.sin(math.radians(angle)))


def inside_range(
    number: float | int, rangeStart: float | int, rangeEnd: float | int
) -> bool:
    return number >= min(rangeStart, rangeEnd) and number <= max(rangeStart, rangeEnd)


def point_circle(point, center, radius: float) -> bool:
    distance = (pygame.Vector2(point) - pygame.Vector2(center)).length()
    return distance <= radius


def rect_circle(rect: pygame.Rect, center, radius: float) -> bool:
    corners = [rect.topleft, rect.bottomleft, rect.topright, rect.bottomright]
    for corner in corners:
        if point_circle(corner, center, radius):
            return True
    return False

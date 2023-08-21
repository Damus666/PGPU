import math, pygame

class Math:
    @staticmethod
    def signof(x):
        return 1 if x > 0 else -1 if x < 0 else 0

    @staticmethod
    def lerp(start, end, t): return (end - start) * t + start

    @staticmethod
    def angle_to_vec(angle:float):
        return pygame.Vector2(math.cos(math.radians(angle)),-math.sin(math.radians(angle)))

    @staticmethod
    def inside_range(number:float|int,rangeStart:float|int,rangeEnd:float|int)->bool:
        return number >= min(rangeStart,rangeEnd) and number <= max(rangeStart,rangeEnd)

    @staticmethod
    def point_circle(point, center, radius):
        distance = (pygame.Vector2(point) - pygame.Vector2(center)).length()
        return distance <= radius

    @staticmethod
    def rect_circle(rect, center, radius):
        corners = [rect.topleft, rect.bottomleft, rect.topright, rect.bottomright]
        for corner in corners:
            if Math.point_circle(corner, center, radius): return True
        return False
    

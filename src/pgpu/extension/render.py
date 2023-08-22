from ..core.window import Window
from ..core.camera import Camera
from ..utils import Vectorizable, Point
import pygame


def rect(rect, color: pygame.Color):
    Window.renderer.draw_color = color
    Window.renderer.draw_rect(rect)


def project_rect(rect: pygame.Rect, color: pygame.Color):
    Window.renderer.draw_color = color
    rect = rect.copy()
    rect.center = rect.center - Camera.position + Window.center
    Window.renderer.draw_rect(rect)


def fill_rect(rect, color: pygame.Color):
    Window.renderer.draw_color = color
    Window.renderer.fill_rect(rect)


def project_filled_rect(rect: pygame.Rect, color: pygame.Color):
    Window.renderer.draw_color = color
    rect = rect.copy()
    rect.center = rect.center - Camera.position + Window.center
    Window.renderer.fill_rect(rect)


def line(point1: Point, point2: Point, color: pygame.Color):
    Window.renderer.draw_color = color
    Window.renderer.draw_line(point1, point2)


def project_line(point1: Vectorizable, point2: Vectorizable, color: pygame.Color):
    Window.renderer.draw_color = color
    point1 = point1 - Camera.position + Window.center
    point2 = point2 - Camera.position + Window.center
    Window.renderer.draw_line(point1, point2)


def point(point: Point, color: pygame.Color):
    Window.renderer.draw_color = color
    Window.renderer.draw_point(point)


def project_point(point: Vectorizable, color: pygame.Color):
    Window.renderer.draw_color = color
    point = point - Camera.position + Window.center
    Window.renderer.draw_point(point)


def quad(
    point1: Point, point2: Point, point3: Point, point4: Point, color: pygame.Color
):
    Window.renderer.draw_color = color
    Window.renderer.draw_quad(point1, point2, point3, point4)


def project_quad(
    point1: Vectorizable,
    point2: Vectorizable,
    point3: Vectorizable,
    point4: Vectorizable,
    color: pygame.Color,
):
    Window.renderer.draw_color = color
    point1 = point1 - Camera.position + Window.center
    point2 = point2 - Camera.position + Window.center
    point3 = point3 - Camera.position + Window.center
    point4 = point4 - Camera.position + Window.center
    Window.renderer.draw_quad(point1, point2, point3, point4)


def fill_quad(
    point1: Point, point2: Point, point3: Point, point4: Point, color: pygame.Color
):
    Window.renderer.draw_color = color
    Window.renderer.fill_quad(point1, point2, point3, point4)


def project_filled_quad(
    point1: Vectorizable,
    point2: Vectorizable,
    point3: Vectorizable,
    point4: Vectorizable,
    color: pygame.Color,
):
    Window.renderer.draw_color = color
    point1 = point1 - Camera.position + Window.center
    point2 = point2 - Camera.position + Window.center
    point3 = point3 - Camera.position + Window.center
    point4 = point4 - Camera.position + Window.center
    Window.renderer.fill_quad(point1, point2, point3, point4)


def triangle(point1: Point, point2: Point, point3: Point, color: pygame.Color):
    Window.renderer.draw_color = color
    Window.renderer.draw_triangle(point1, point2, point3)


def project_triangle(
    point1: Vectorizable,
    point2: Vectorizable,
    point3: Vectorizable,
    color: pygame.Color,
):
    Window.renderer.draw_color = color
    point1 = point1 - Camera.position + Window.center
    point2 = point2 - Camera.position + Window.center
    point3 = point3 - Camera.position + Window.center
    Window.renderer.draw_triangle(point1, point2, point3)


def fill_triangle(point1: Point, point2: Point, point3: Point, color: pygame.Color):
    Window.renderer.draw_color = color
    Window.renderer.fill_triangle(point1, point2, point3)


def project_filled_triangle(
    point1: Vectorizable,
    point2: Vectorizable,
    point3: Vectorizable,
    color: pygame.Color,
):
    Window.renderer.draw_color = color
    point1 = point1 - Camera.position + Window.center
    point2 = point2 - Camera.position + Window.center
    point3 = point3 - Camera.position + Window.center
    Window.renderer.fill_triangle(point1, point2, point3)

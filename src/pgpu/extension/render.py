from ..core.window import Window
from ..utils import classproperty
import pygame


def rect(rect, color: pygame.Color):
    Window.renderer.draw_color = color
    Window.renderer.draw_rect(rect)


def fill_rect(rect, color: pygame.Color):
    Window.renderer.draw_color = color
    Window.renderer.fill_rect(rect)


def line(point1, point2, color: pygame.Color):
    Window.renderer.draw_color = color
    Window.renderer.draw_line(point1, point2)


def point(point, color: pygame.Color):
    Window.renderer.draw_color = color
    Window.renderer.draw_point(point)


def quad(point1, point2, point3, point4, color: pygame.Color):
    Window.renderer.draw_color = color
    Window.renderer.draw_quad(point1, point2, point3, point4)


def fill_quad(point1, point2, point3, point4, color: pygame.Color):
    Window.renderer.draw_color = color
    Window.renderer.fill_quad(point1, point2, point3, point4)


def triangle(point1, point2, point3, color: pygame.Color):
    Window.renderer.draw_color = color
    Window.renderer.draw_triangle(point1, point2, point3)


def fill_triangle(point1, point2, point3, color: pygame.Color):
    Window.renderer.draw_color = color
    Window.renderer.fill_triangle(point1, point2, point3)

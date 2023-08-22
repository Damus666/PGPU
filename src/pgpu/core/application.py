from .window import Window
from .time import Time
from .input import Input
from ..component.scene import Scenes
import pygame, sys
import pygame._sdl2 as pgsdl


class Application:
    @classmethod
    def init(
        cls,
        sdl_window: pgsdl.Window,
        target_fps: int = 0,
        accelerated: bool = True,
        input_elasticity: float = 1.5,
    ):
        Window._init(sdl_window, accelerated)
        Time._init(target_fps)
        Input._init(input_elasticity)

    @classmethod
    def run(cls):
        while True:
            events = pygame.event.get()
            Time._update()
            Input._update(events)

            for event in events:
                if event.type == pygame.QUIT:
                    Scenes.scene.on_quit()
                    pygame.quit()
                    sys.exit()
                Input._event(event)
                Scenes.scene.event(event)

            Window.renderer.draw_color = Scenes.scene.skybox_color
            Window.renderer.clear()

            Scenes.scene.update()
            Scenes.scene.draw()
            Scenes.scene.render()

            Window.renderer.present()

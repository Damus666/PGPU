from pgpu import *
from menu_scene import menu_scene

Application.init(
    SDLWindow(
        "Pong Demo",
        (system.SCREEN_RESOLUTION.x // 1.5, system.SCREEN_RESOLUTION.y // 1.5),
    ),
    0,
    True,
    3,
)

menu_scene()

Application.run()

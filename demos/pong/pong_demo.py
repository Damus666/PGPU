from pgpu import *
from menu_scene import menu_scene
from main_scene import main_scene

Application.init(
    SDLWindow(
        "Pong Demo",
        (system.SCREEN_RESOLUTION.x // 1.5, system.SCREEN_RESOLUTION.y // 1.5),
    ),
    60, True, 3,
)
Scenes.register_scene_funcs(menu_scene, main_scene)
Scenes.call_scene_func("menu_scene")

Application.run()

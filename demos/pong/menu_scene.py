from pgpu import *
from menu import MenuEntity


def menu_scene():
    Scenes.new_scene(SceneConfig((30, 30, 30)))
    MenuEntity.instantiate()

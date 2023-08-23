from pgpu import *
from main import ManagerEntity, PlatformEntity, BallEntity


def main_scene():
    Scenes.new_scene(
        SceneConfig((30, 30, 30), ["visible-main"], [], ["player", "enemy", "ball"])
    )
    ManagerEntity.instantiate()
    BallEntity.instantiate()
    PlatformEntity.instantiate("player", True)
    PlatformEntity.instantiate("enemy", False)

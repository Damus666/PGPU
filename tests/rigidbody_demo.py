from pgpu import *


class Player(Component):
    unique = True

    def init(self):
        self.main_collider = self.entity.add_collider((100, 100), (0, 0))

    def update(self):
        self.entity.speed += (
            vector(Input.get_axis("horizontal"), Input.get_axis("vertical")) * 0.5
        )
        Camera.position = self.transform.position

    def render(self):
        render.project_rect(self.main_collider._old_box, Color("red"))
        render.project_rect(self.main_collider.box, Color("blue"))


class PlayerHitCallbacks(RigidbodyCallbacks):
    def on_collision_exit(self, collider: Collider):
        ...#print("c exit")

    def on_collision_enter(self, collider: Collider):
        ...#print("c enter")

    def on_collision_stay(self, collider: Collider):
        ...#print("c stay")


class PlayerEntity(RigidbodyEntity):
    unique = True
    start_components = [Player]

    @classmethod
    def instantiate(cls):
        player = PlayerEntity(
            Transform(),
            ["visible-main", "updates", "rendering"],
            graphics.empty_texture((100, 100), "green"),
            ["player"],
            callbacks_type=PlayerHitCallbacks,
            is_static=False,
            gravity_scale=100
        )
        return player


class ObstacleEntity(RigidbodyEntity):
    unique = True

    @classmethod
    def instantiate(cls):
        obstacle = ObstacleEntity(
            Transform(vector(-200, 0)),
            ["visible-main", "updates"],
            graphics.empty_texture((200, 50), "red"),
            is_static=False,
        )
        obstacle.add_collider((200, 50), (0, 0))
        obstacle.speed = vector(30,0)
        return obstacle
    
    def update(self):
        self.speed.x = 30
        return super().update()


def main_scene():
    Scenes.new_scene(SceneConfig(tags=["player"]))
    PlayerEntity.instantiate()
    ObstacleEntity.instantiate()
    ob = RigidbodyEntity(Transform(vector(-300,-300)), ["visible-main"], graphics.empty_texture((200,200), "pink"))
    ob.add_collider((200,200))


Application.init(SDLWindow("Rigidbody Demo", (1000, 650)))
main_scene()
Application.run()

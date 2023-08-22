from pgpu import *


class const:
    amount = 40
    speed = 300
    anim_speed = 6


class AssetLoader:
    assets = {}

    @classmethod
    def load(cls):
        cls.assets["grass"] = graphics.load("tests/grass.png", 1)


class Manager(Component):
    unique = True

    def init(self):
        self.speed = const.speed

    def update(self):
        Window.window.title = f"{Time.framerate:.0f}"
        Camera.position = self.transform.position

        self.transform.position += (
            vector(Input.get_axis("horizontal"), Input.get_axis("vertical"))
            * self.speed
            * Time.delta_time
        )
    
    def render(self):
        render.project_line((-100,0), (100,0), pygame.Color("green"))
        render.project_rect(pygame.Rect(0,0,200,200), pygame.Color("yellow"))

class ManagerEntity(Entity):
    start_components = [Manager, Animator]
    unique = True

    def init(self):
        self.Animator.setup(
            [
                graphics.empty_texture(color=col)
                for col in ["green", "red", "blue", "purple"]
            ],
            const.anim_speed,
        )

    @classmethod
    def instantiate(cls):
        return ManagerEntity(
            Transform(),
            ["updates", "event-handler", "quit-handler", "visible-top", "rendering"],
            AssetLoader.assets["grass"],
        )


class Particle(Component):
    def update(self):
        self.transform.rotation += 100 * Time.delta_time


class ParticleEntity(Entity):
    start_components = [Particle]

    @classmethod
    def instantiate(cls, pos):
        return ParticleEntity(
            Transform(
                pos + rand.rand_offset_vec(10),
                (random.uniform(0.5, 2.0), random.uniform(1.0, 2.0)),
            ),
            ["visible-main", "updates"],
            graphics.empty_texture((10, 10), graphics.random_color()),
        )


def main_scene():
    Scenes.new_scene(SceneConfig((0, 0, 150), ["visible-main", "visible-top"]))
    ManagerEntity.instantiate()
    amount = const.amount
    spacing = Window.bounds.w // amount
    for x in range(amount):
        for y in range(amount):
            ParticleEntity.instantiate(
                (x * spacing - Window.bounds.w // 2, y * spacing - Window.bounds.h // 2)
            )


Application.init(SDLWindow("Test", (1000, 650)))
AssetLoader.load()
main_scene()
Application.run()

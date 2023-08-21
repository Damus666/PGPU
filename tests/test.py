from pgpu import *

class const:
    amount=30
    speed=300
    anim_speed = 6

class Manager(Component):
    unique = True

    def init(self):
        self.speed = const.speed

    def update(self):
        Window.window.title = f"{Time.framerate:.0f}"
        Camera.position = self.transform.position-Window.center

        self.transform.position += vector(Input.get_axis("horizontal"), Input.get_axis("vertical"))*self.speed*Time.delta_time

    def render(self):
        Render.fill_rect((10,10,300,100), Color(30,67,156))

class ManagerEntity(Entity):
    start_components = [Manager, Animator]
    unique = True

    def init(self):
        self.Animator.setup([Graphics.empty_texture(color=col) for col in ["green", "red", "blue", "purple"]], const.anim_speed)

    @classmethod
    def instantiate(cls):
        return ManagerEntity(Transform(), 
                             ["updates", "event-handler", "quit-handler", "visible-top", "rendering"], 
                             Graphics.empty_texture(color="green"))
    
class Particle(Component):
    def update(self):
        self.transform.rotation += 100*Time.delta_time
    
class ParticleEntity(Entity):
    start_components = [Particle]

    @classmethod
    def instantiate(cls, pos):
        return ParticleEntity(Transform(pos+Random.rand_offset_vec(10),(random.uniform(0.5,2.0), random.uniform(1.0,2.0))),
                              ["visible-main", "updates"], Graphics.empty_texture((10,10), Graphics.random_color()))

def main_scene():
    Scenes.new_scene(SceneConfig("blue", ["visible-main", "visible-top"]))
    ManagerEntity.instantiate()
    amount = const.amount
    spacing = Window.bounds.w//amount
    for x in range(amount):
        for y in range(amount):
            ParticleEntity.instantiate((x*spacing-Window.bounds.w//2, y*spacing-Window.bounds.h//2))

Application.init(SDLWindow("Test", (1000, 650)))
main_scene()
Application.run()
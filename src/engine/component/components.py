import typing
import pygame._sdl2 as pgsdl
from ..core.time import Time
if typing.TYPE_CHECKING:
    from component.scene import Entity

class Component:
    instance=None
    unique = False

    def __init__(self, entity):
        self.entity:"Entity" = entity
        self.transform = self.entity.transform
        if self.unique:
            self.__class__.instance = self
            setattr(self.entity, self.__class__.__name__, self)
    
    def on_destroy(self):...
    def init(self): ...
    def update(self): ...
    def event(self, event): ...
    def on_quit(self): ...
    def render(self): ...

    def destroy(self):
        for comp_name, comp in list(self.entity.components.items()):
            if comp is self: del self.entity.components[comp_name]
        del self

class Animator(Component):
    unique = True

    def init(self):
        self.has_setup = False

    def setup(self, textures:list[pgsdl.Texture], animation_speed:float=1, loop:bool=True, on_finish=None):
        self.textures = textures
        self.frame_index = 0
        self.animation_speed = animation_speed
        self.original_texture = self.entity.texture
        self.loop = loop
        self.on_finish = on_finish
        self.has_setup = True

    def update(self):
        if not self.has_setup: return False
        self.frame_index += self.animation_speed*Time.delta_time
        if self.frame_index >= len(self.textures):
            if self.loop:
                self.frame_index = 0
            else:
                self.frame_index = len(self.textures)-1
                if self.on_finish: self.on_finish()
                else: self.entity.destroy()
        self.entity.texture = self.textures[int(self.frame_index)]

    def stop_loop(self, on_finish=None):
        self.loop = False
        self.on_finish = on_finish

    def resume_loop(self):
        self.loop = True
        self.on_finish = None

class StatusAnimator(Animator):
    def setup(self, animations:dict[str,list[pgsdl.Texture]], status:str, animation_speed:float=1, loop:bool=True, on_finish=None):
        self.animations = animations
        self.status = status
        super().setup(self.animations[self.status], animation_speed, loop, on_finish)

    def set_status(self, status):
        if not self.has_setup: return False
        if status != self.status:
            self.status = status
            self.textures = self.animations[self.status]
            return True
        return False
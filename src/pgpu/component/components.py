import typing, pygame
import pygame._sdl2 as pgsdl
from typing import Callable
from ..core.time import Time
from ..utils import Vectorizable

if typing.TYPE_CHECKING:
    from ..component.scene import Entity
    from ..component.entities import RigidbodyEntity


class Component:
    instance: "Component" = None
    unique: bool = False

    def __init__(self, entity: "Entity"):
        self.entity: "Entity"|"RigidbodyEntity" = entity
        self.transform = self.entity.transform
        self.id = self.entity.scene._id
        self.entity.scene._id += 1
        if self.unique:
            self.__class__.instance = self
            setattr(self.entity, self.__class__.__name__, self)

    def on_destroy(self):
        ...

    def init(self):
        ...

    def update(self):
        ...

    def event(self, event: pygame.event.Event):
        ...

    def on_quit(self):
        ...

    def render(self):
        ...

    def destroy_after(self, time_ms:int):
        Time.invoke(self.destroy, time_ms, f"{self.__str__()}_Destroy")

    def destroy(self):
        for comp_name, (single, multiple) in list(self.entity.components.items()):
            if single is self:
                del self.entity.components[comp_name]
            else:
                if self in multiple:
                    self.entity.components[comp_name][1].remove(self)
                    if len(self.entity.components[comp_name][1]) == 1:
                        self.entity.components[comp_name][0] = self.entity.components[
                            comp_name
                        ][1][0]
                        self.entity.components[comp_name][1] = []
        del self


class Animator(Component):
    unique = True

    def init(self):
        self.has_setup: bool = False

    def setup(
        self,
        textures: list[pgsdl.Texture],
        animation_speed: float = 1,
        loop: bool = True,
        on_finish: Callable = None,
    ):
        self.textures: list[pgsdl.Texture] = textures
        self.frame_index: float = 0
        self.animation_speed: float = animation_speed
        self.original_texture: pgsdl.Texture = self.entity.texture
        self.loop: bool = loop
        self.on_finish: Callable | None = on_finish
        self.has_setup: bool = True

    def update(self):
        if not self.has_setup:
            return False
        self.frame_index += self.animation_speed * Time.delta_time
        if self.frame_index >= len(self.textures):
            if self.loop:
                self.frame_index = 0
            else:
                self.frame_index = len(self.textures) - 1
                if self.on_finish:
                    self.on_finish()
                else:
                    self.entity.destroy()
        self.entity.texture = self.textures[int(self.frame_index)]

    def stop_loop(self, on_finish: Callable = None):
        self.loop = False
        self.on_finish = on_finish

    def resume_loop(self):
        self.loop = True
        self.on_finish = None


class StatusAnimator(Animator):
    def setup(
        self,
        animations: dict[str, list[pgsdl.Texture]],
        status: str,
        animation_speed: float = 1,
        loop: bool = True,
        on_finish: Callable = None,
    ):
        self.animationsdict[str, list[pgsdl.Texture]] = animations
        self.status: str = status
        super().setup(self.animations[self.status], animation_speed, loop, on_finish)

    def set_status(self, status: str):
        if not self.has_setup:
            return False
        if status != self.status:
            self.status = status
            self.textures = self.animations[self.status]
            return True
        return False
    
class Collider(Component):
    def init(self):
        self.rigidbody:"RigidbodyEntity" = self.entity
        self.size = pygame.Vector2(10,10)
        self.offset = pygame.Vector2(0,0)
        self.box = pygame.FRect((0,0), self.size)
        self.is_trigger:bool = False
        self.box.center = self.entity.transform.position+self.offset
        self._old_box = self.box.copy()

    def setup(self, size:Vectorizable=None, offset:Vectorizable=None, is_trigger:bool=False):
        self.rigidbody:"RigidbodyEntity" = self.entity
        self.size = pygame.Vector2(10,10) if size is None else pygame.Vector2(size)
        self.offset = pygame.Vector2(0,0) if offset is None else pygame.Vector2(offset)
        self.box = pygame.FRect((0,0), self.size)
        self.is_trigger:bool = is_trigger
        self.box.center = self.transform.position+self.offset
        self._old_box = self.box.copy()

    def change_size(self, size:Vectorizable):
        self.size = pygame.Vector2(size)
        self.box.size = self.size
        self.box.center = self.transform.position+self.offset

    def _update_old(self):
        if Time.ticks % 20 != 0: return
        self._old_box.size = self.box.size
        self._old_box.center = self.box.center

    def destroy(self):
        if self in self.entity._colliders: self.entity._colliders.remove(self)
        return super().destroy()

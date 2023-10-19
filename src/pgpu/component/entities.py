import pygame
import pygame._sdl2 as pgsdl

from ..core.physics import _Physics
from ..core.time import Time
from ..utils import Vectorizable
from .components import Collider
from .scene import Entity
from .transform import Transform


class RigidbodyCallbacks:
    default: "RigidbodyCallbacks" = None

    def __init__(self, rigidbody):
        self.rigidbody = rigidbody

    def on_collision_enter(self, collider: Collider):
        ...

    def on_collision_stay(self, collider: Collider):
        ...

    def on_collision_exit(self, collider: Collider):
        ...

    def on_trigger_enter(self, collider: Collider):
        ...

    def on_trigger_stay(self, collider: Collider):
        ...

    def on_trigger_exit(self, collider: Collider):
        ...


RigidbodyCallbacks.default = RigidbodyCallbacks(None)


class RigidbodyEntity(Entity):
    def __init__(
        self,
        transform: Transform,
        layer_names: list[str],
        texture: pgsdl.Texture = None,
        tags: list[str] = None,
        callbacks_type: type[RigidbodyCallbacks] = None,
        is_static: bool = True,
        gravity_scale: float = 0,
    ):
        self._super_entity = super()
        self._callbacks = (
            callbacks_type(self)
            if callbacks_type is not None
            else RigidbodyCallbacks.default
        )
        self._hystory = {}
        self._colliders: list[Collider] = []

        self.acceleration: pygame.Vector2 = pygame.Vector2()
        self.speed: pygame.Vector2 = pygame.Vector2()
        self.is_static: bool = is_static
        self.gravity_scale: float = gravity_scale
        _Physics._register_body(self)

        self._super_entity.__init__(transform, layer_names, texture, tags)

    def destroy(self):
        _Physics._destroyed_body(self)
        self._super_entity.destroy()

    def update(self):
        if not self.is_static:
            for collider in self._colliders:
                collider._update_old()
            self.speed.x += self.acceleration.x * Time.delta_time
            self.transform.position.x += self.speed.x * Time.delta_time
            self._snap_colliders()
            self._collisions("h")
            self.speed.y += (
                self.acceleration.y * Time.delta_time
                + self.gravity_scale * Time.delta_time
            )
            self.transform.position.y += self.speed.y * Time.delta_time
            self._snap_colliders()
            self._collisions("v")
        self.acceleration = pygame.Vector2()

    def _collisions(self, direction):
        for collider in self._colliders:
            for body in _Physics._rigidbodies:
                if body is self:
                    continue
                for other in body._colliders:
                    if not other.id in self._hystory:
                        self._hystory[other.id] = {"h": False, "v": False}
                    if other.box.colliderect(collider.box):
                        if not collider.is_trigger:
                            if direction == "h":
                                self._resolve_collisions_h(collider, other, body)
                            elif direction == "v":
                                self._resolve_collisions_v(collider, other, body)
                        if self._hystory[other.id][direction]:
                            self._callbacks.on_collision_stay(
                                other
                            ) if not collider.is_trigger else self._callbacks.on_trigger_stay(
                                other
                            )
                            body._callbacks.on_collision_stay(
                                collider
                            ) if not other.is_trigger else body._callbacks.on_trigger_stay(
                                collider
                            )
                        else:
                            self._callbacks.on_collision_enter(
                                other
                            ) if not collider.is_trigger else self._callbacks.on_trigger_enter(
                                other
                            )
                            body._callbacks.on_collision_enter(
                                collider
                            ) if not other.is_trigger else body._callbacks.on_trigger_enter(
                                collider
                            )
                        self._hystory[other.id][direction] = True
                    else:
                        if self._hystory[other.id][direction]:
                            self._callbacks.on_collision_exit(
                                other
                            ) if not collider.is_trigger else self._callbacks.on_trigger_exit(
                                other
                            )
                            body._callbacks.on_collision_exit(
                                collider
                            ) if not other.is_trigger else body._callbacks.on_trigger_exit(
                                collider
                            )
                        self._hystory[other.id][direction] = False

    def _resolve_collisions_h(
        self, collider: Collider, other: Collider, body: "RigidbodyEntity"
    ):
        if body.is_static:
            collider.box.left = (
                other.box.right if self.speed.x < 0 else collider.box.left
            )
            collider.box.right = (
                other.box.left if self.speed.x > 0 else collider.box.right
            )
        else:
            if (
                collider.box.left < other.box.right
                and collider._old_box.left >= other.box.right
            ):
                collider.box.left = other.box.right
            if (
                collider.box.right > other.box.left
                and collider._old_box.right <= other.box.left
            ):
                collider.box.right = other.box.left
        self.acceleration.x = 0
        self.speed.x = 0
        self.transform.position.x = collider.box.centerx - collider.offset.x
        self._snap_colliders()

    def _resolve_collisions_v(
        self, collider: Collider, other: Collider, body: "RigidbodyEntity"
    ):
        if body.is_static:
            collider.box.top = (
                other.box.bottom if self.speed.y < 0 else collider.box.top
            )
            collider.box.bottom = (
                other.box.top if self.speed.y > 0 else collider.box.bottom
            )
        else:
            if (
                collider.box.top < other.box.bottom
                and collider._old_box.top >= other.box.bottom
            ):
                collider.box.top = other.box.bottom
            if (
                collider.box.bottom > other.box.top
                and collider._old_box.bottom <= other.box.top
            ):
                collider.box.bottom = other.box.top
        self.acceleration.y = 0
        self.speed.y = 0
        self.transform.position.y = collider.box.centery - collider.offset.y
        self._snap_colliders()

    def _snap_colliders(self):
        for collider in self._colliders:
            collider.box.center = self.transform.position + collider.offset

    def add_collider(
        self,
        size: Vectorizable = None,
        offset: Vectorizable = None,
        is_trigger: bool = False,
    ) -> Collider:
        collider: Collider = self.add_component(Collider, init_component=False)
        collider.setup(size, offset, is_trigger)
        self._colliders.append(collider)
        return collider

    def add_acceleration(self, acceleration: Vectorizable):
        self.acceleration += pygame.Vector2(acceleration)

    def add_force(self, force: Vectorizable):
        self.acceleration += pygame.Vector2(force) / self.mass

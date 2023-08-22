import typing, pygame
from ..component.scene import Scenes, Entity
from ..extension import mathf
from ..utils import Vectorizable

if typing.TYPE_CHECKING:
    from ..component.entities import RigidbodyEntity
    from ..component.components import CastTarget, Collider


class _Physics:
    _rigidbodies: list["RigidbodyEntity"] = []
    _cast_targets: list["CastTarget"] = []

    @classmethod
    def _register(cls, rigidbody: "RigidbodyEntity"):
        cls._rigidbodies.append(rigidbody)

    @classmethod
    def _destroyed(cls, rigidbody: "RigidbodyEntity"):
        if rigidbody in cls._rigidbodies:
            cls._rigidbodies.remove(rigidbody)

    @classmethod
    def _register_target(cls, target: "CastTarget"):
        cls._cast_targets.append(target)

    @classmethod
    def _destroyed_target(cls, target: "CastTarget"):
        if target in cls._cast_targets:
            cls._cast_targets.remove(target)


class CastFilter:
    def __init__(
        self,
        include_layers: list[str] = None,
        exclude_layers: list[str] = None,
        include_tags: list[str] = None,
        exclude_tags: list[str] = None,
        include_cast_layers: list[str] = None,
        exclude_cast_layers: list[str] = None,
    ):
        self.include_layers = (
            include_layers
            if include_layers is not None
            else list(Scenes.scene.layers.keys())
        )
        self.exclude_layes = exclude_layers if exclude_layers is not None else []
        self.include_tags = (
            set(include_tags)
            if include_tags is not None
            else set(Scenes.scene.tags.keys())
        )
        self.exclude_tags = set(exclude_tags) if exclude_tags is not None else set()
        self.include_cast_layers = include_cast_layers
        self.exclude_cast_layers = (
            exclude_cast_layers if exclude_cast_layers is not None else []
        )

    def layers(self):
        return [
            layer
            for layer in Scenes.scene.layers.values()
            if layer.name in self.include_layers
            and layer.name not in self.exclude_layes
        ]


def ray_cast(
    start: Vectorizable, direction: Vectorizable, length: float, cast_filter: CastFilter
) -> Entity:
    start = pygame.Vector2(start)
    end = start + pygame.Vector2(direction) * length
    for layer in cast_filter.layers():
        for entity in layer.entities:
            if not (entity_tags := set(entity.tags)).intersection(
                cast_filter.include_tags
            ):
                continue
            if entity_tags.intersection(cast_filter.exclude_tags):
                continue
            if mathf.line_rect(start, end, entity.box):
                return entity


def ray_cast_all(
    start: Vectorizable, direction: Vectorizable, length: float, cast_filter: CastFilter
) -> list[Entity]:
    start = pygame.Vector2(start)
    end = start + pygame.Vector2(direction) * length
    entities = []
    for layer in cast_filter.layers():
        for entity in layer.entities:
            if not (entity_tags := set(entity.tags)).intersection(
                cast_filter.include_tags
            ):
                continue
            if entity_tags.intersection(cast_filter.exclude_tags):
                continue
            if mathf.line_rect(start, end, entity.box):
                entities.append(entity)
    return entities


def ray_cast_targets(
    start: Vectorizable, direction: Vectorizable, length: float, cast_filter: CastFilter
) -> Entity:
    start = pygame.Vector2(start)
    end = start + pygame.Vector2(direction) * length
    for target in _Physics._cast_targets:
        if (
            cast_filter.include_cast_layers is not None
            and not target.cast_layer in cast_filter.include_cast_layers
        ):
            continue
        if target.cast_layer in cast_filter.exclude_cast_layers:
            continue
        if mathf.line_rect(start, end, target.entity.box):
            return target.entity


def ray_cast_all_targets(
    start: Vectorizable, direction: Vectorizable, length: float, cast_filter: CastFilter
) -> list[Entity]:
    start = pygame.Vector2(start)
    end = start + pygame.Vector2(direction) * length
    entities = []
    for target in _Physics._cast_targets:
        if (
            cast_filter.include_cast_layers is not None
            and not target.cast_layer in cast_filter.include_cast_layers
        ):
            continue
        if target.cast_layer in cast_filter.exclude_cast_layers:
            continue
        if mathf.line_rect(start, end, target.entity.box):
            entities.append(target.entity)
    return entities


def ray_cast_bodies(
    start: Vectorizable, direction: Vectorizable, length: float, cast_filter: CastFilter
) -> "Collider":
    start = pygame.Vector2(start)
    end = start + pygame.Vector2(direction) * length
    for body in _Physics._rigidbodies:
        if not (entity_tags := set(body.tags)).intersection(cast_filter.include_tags):
            continue
        if entity_tags.intersection(cast_filter.exclude_tags):
            continue
        for collider in body._colliders:
            if mathf.line_rect(start, end, collider.box):
                return collider


def ray_cast_all_bodies(
    start: Vectorizable, direction: Vectorizable, length: float, cast_filter: CastFilter
) -> list["Collider"]:
    start = pygame.Vector2(start)
    end = start + pygame.Vector2(direction) * length
    colliders = []
    for body in _Physics._rigidbodies:
        if not (entity_tags := set(body.tags)).intersection(cast_filter.include_tags):
            continue
        if entity_tags.intersection(cast_filter.exclude_tags):
            continue
        for collider in body._colliders:
            if mathf.line_rect(start, end, collider.box):
                colliders.append(collider)
    return colliders


def line_cast(
    start: Vectorizable, end: Vectorizable, cast_filter: CastFilter
) -> Entity:
    for layer in cast_filter.layers():
        for entity in layer.entities:
            if not (entity_tags := set(entity.tags)).intersection(
                cast_filter.include_tags
            ):
                continue
            if entity_tags.intersection(cast_filter.exclude_tags):
                continue
            if mathf.line_rect(start, end, entity.box):
                return entity


def line_cast_all(
    start: Vectorizable, end: Vectorizable, cast_filter: CastFilter
) -> list[Entity]:
    if cast_filter is None:
        cast_filter = CastFilter.default
    entities = []
    for layer in cast_filter.layers():
        for entity in layer.entities:
            if not (entity_tags := set(entity.tags)).intersection(
                cast_filter.include_tags
            ):
                continue
            if entity_tags.intersection(cast_filter.exclude_tags):
                continue
            if mathf.line_rect(start, end, entity.box):
                entities.append(entity)
    return entities


def line_cast_targets(
    start: Vectorizable, end: Vectorizable, cast_filter: CastFilter
) -> Entity:
    for target in _Physics._cast_targets:
        if (
            cast_filter.include_cast_layers is not None
            and not target.cast_layer in cast_filter.include_cast_layers
        ):
            continue
        if target.cast_layer in cast_filter.exclude_cast_layers:
            continue
        if mathf.line_rect(start, end, target.entity.box):
            return target.entity


def line_cast_all_targets(
    start: Vectorizable, end: Vectorizable, cast_filter: CastFilter
) -> list[Entity]:
    entities = []
    for target in _Physics._cast_targets:
        if (
            cast_filter.include_cast_layers is not None
            and not target.cast_layer in cast_filter.include_cast_layers
        ):
            continue
        if target.cast_layer in cast_filter.exclude_cast_layers:
            continue
        if mathf.line_rect(start, end, target.entity.box):
            entities.append(target.entity)
    return entities


def line_cast_bodies(
    start: Vectorizable, end: Vectorizable, cast_filter: CastFilter
) -> "Collider":
    for body in _Physics._rigidbodies:
        if not (entity_tags := set(body.tags)).intersection(cast_filter.include_tags):
            continue
        if entity_tags.intersection(cast_filter.exclude_tags):
            continue
        for collider in body._colliders:
            if mathf.line_rect(start, end, collider.box):
                return collider


def line_cast_all_bodies(
    start: Vectorizable, end: Vectorizable, cast_filter: CastFilter
) -> list["Collider"]:
    colliders = []
    for body in _Physics._rigidbodies:
        if not (entity_tags := set(body.tags)).intersection(cast_filter.include_tags):
            continue
        if entity_tags.intersection(cast_filter.exclude_tags):
            continue
        for collider in body._colliders:
            if mathf.line_rect(start, end, collider.box):
                colliders.append(collider)
    return colliders


def circle_cast(center: Vectorizable, radius: float, cast_filter: CastFilter) -> Entity:
    for layer in cast_filter.layers():
        for entity in layer.entities:
            if not (entity_tags := set(entity.tags)).intersection(
                cast_filter.include_tags
            ):
                continue
            if entity_tags.intersection(cast_filter.exclude_tags):
                continue
            if mathf.rect_circle(entity.box, center, radius):
                return entity


def circle_cast_all(
    center: Vectorizable, radius: float, cast_filter: CastFilter
) -> list[Entity]:
    entities = []
    for layer in cast_filter.layers():
        for entity in layer.entities:
            if not (entity_tags := set(entity.tags)).intersection(
                cast_filter.include_tags
            ):
                continue
            if entity_tags.intersection(cast_filter.exclude_tags):
                continue
            if mathf.rect_circle(entity.box, center, radius):
                entities.append(entity)
    return entities


def circle_cast_targets(
    center: Vectorizable, radius: float, cast_filter: CastFilter
) -> Entity:
    for target in _Physics._cast_targets:
        if (
            cast_filter.include_cast_layers is not None
            and not target.cast_layer in cast_filter.include_cast_layers
        ):
            continue
        if target.cast_layer in cast_filter.exclude_cast_layers:
            continue
        if mathf.rect_circle(target.entity.box, center, radius):
            return target.entity


def circle_cast_all_targets(
    center: Vectorizable, radius: float, cast_filter: CastFilter
) -> list[Entity]:
    entities = []
    for target in _Physics._cast_targets:
        if (
            cast_filter.include_cast_layers is not None
            and not target.cast_layer in cast_filter.include_cast_layers
        ):
            continue
        if target.cast_layer in cast_filter.exclude_cast_layers:
            continue
        if mathf.rect_circle(target.box, center, radius):
            entities.append(target.entity)
    return entities


def circle_cast_bodies(
    center: Vectorizable, radius: float, cast_filter: CastFilter
) -> "Collider":
    for body in _Physics._rigidbodies:
        if not (entity_tags := set(body.tags)).intersection(cast_filter.include_tags):
            continue
        if entity_tags.intersection(cast_filter.exclude_tags):
            continue
        for collider in body._colliders:
            if mathf.rect_circle(collider.box, center, radius):
                return collider


def circle_cast_all_bodies(
    center: Vectorizable, radius: float, cast_filter: CastFilter
) -> list["Collider"]:
    if cast_filter is None:
        cast_filter = CastFilter.default
    colliders = []
    for body in _Physics._rigidbodies:
        if not (entity_tags := set(body.tags)).intersection(cast_filter.include_tags):
            continue
        if entity_tags.intersection(cast_filter.exclude_tags):
            continue
        for collider in body._colliders:
            if mathf.rect_circle(collider.box, center, radius):
                colliders.append(collider)
    return colliders


def box_cast(box: pygame.Rect, cast_filter: CastFilter) -> Entity:
    for layer in cast_filter.layers():
        for entity in layer.entities:
            if not (entity_tags := set(entity.tags)).intersection(
                cast_filter.include_tags
            ):
                continue
            if entity_tags.intersection(cast_filter.exclude_tags):
                continue
            if entity.box.colliderect(box):
                return entity


def box_cast_all(box: pygame.Rect, cast_filter: CastFilter) -> list[Entity]:
    entities = []
    for layer in cast_filter.layers():
        for entity in layer.entities:
            if not (entity_tags := set(entity.tags)).intersection(
                cast_filter.include_tags
            ):
                continue
            if entity_tags.intersection(cast_filter.exclude_tags):
                continue
            if entity.box.colliderect(box):
                entities.append(entity)
    return entities


def box_cast_targets(box: pygame.Rect, cast_filter: CastFilter) -> Entity:
    for target in _Physics._cast_targets:
        if (
            cast_filter.include_cast_layers is not None
            and not target.cast_layer in cast_filter.include_cast_layers
        ):
            continue
        if target.cast_layer in cast_filter.exclude_cast_layers:
            continue
        if target.entity.box.colliderect(box):
            return target.entity


def box_cast_all_targets(box: pygame.Rect, cast_filter: CastFilter) -> list[Entity]:
    entities = []
    for target in _Physics._cast_targets:
        if (
            cast_filter.include_cast_layers is not None
            and not target.cast_layer in cast_filter.include_cast_layers
        ):
            continue
        if target.cast_layer in cast_filter.exclude_cast_layers:
            continue
        if target.entity.box.colliderect(box):
            entities.append(target.entity)
    return entities


def box_cast_bodies(box: pygame.Rect, cast_filter: CastFilter) -> "Collider":
    for body in _Physics._rigidbodies:
        if not (entity_tags := set(body.tags)).intersection(cast_filter.include_tags):
            continue
        if entity_tags.intersection(cast_filter.exclude_tags):
            continue
        for collider in body._colliders:
            if collider.box.colliderect(box):
                return collider


def box_cast_all_bodies(box: pygame.Rect, cast_filter: CastFilter) -> list["Collider"]:
    colliders = []
    for body in _Physics._rigidbodies:
        if not (entity_tags := set(body.tags)).intersection(cast_filter.include_tags):
            continue
        if entity_tags.intersection(cast_filter.exclude_tags):
            continue
        for collider in body._colliders:
            if collider.box.colliderect(box):
                colliders.append(collider)
    return colliders

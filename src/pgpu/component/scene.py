from typing import Callable, Self

import pygame
import pygame._sdl2 as pgsdl

from ..core.camera import Camera
from ..core.window import Window
from .components import Component
from .transform import Transform


class Entity:
    start_components: list[type[Component] | list[str, type[Component]]] = []
    instance: "Entity" = None
    unique: bool = False

    def __init__(
        self,
        transform: Transform,
        layer_names: list[str],
        texture: pgsdl.Texture = None,
        tags: list[str] = None,
    ):
        # scene
        self.scene: Scene = Scenes.scene
        self.id = self.scene._id
        self.scene._id += 1
        # transform
        self.transform: Transform = transform
        # layers
        self.layers: dict[str, Layer] = {}
        if not "all" in layer_names:
            layer_names.append("all")
        for layer in layer_names:
            self.scene.layers[layer].add(self)
        # name
        self.name: str = self.__class__.__name__
        # texture
        self.texture: pgsdl.Texture | None = texture
        # box
        self.box = pygame.Rect(0, 0, 0, 0)
        # tags
        self.tags: list[str] = []
        tags = tags if tags is not None else []
        for tag in tags:
            self.add_tag(tag)
        # components
        self._components: dict[str, list[Component | None, list[Component]]] = {}
        for comp in self.start_components:
            if isinstance(comp, list):
                comp_name, comp_type = comp
            else:
                comp_name, comp_type = comp.__name__, comp
            self.add_component(comp_type, comp_name, False)
        for single, multiple in list(self._components.values()):
            if single is not None:
                single.init()
            else:
                for c in multiple:
                    c.init()
        # unique
        if self.unique:
            self.__class__.instance = self
            setattr(self.scene, self.__class__.__name__, self)
        # init
        self.init()

    # builtin
    def in_layer(self, name: str) -> bool:
        return name in self.layers

    def add_layer(self, name: str):
        self.scene.layers[name].add(self)

    def remove_layer(self, name: str):
        self.scene.layers[name].remove(self)

    def add_tag(self, tag: str):
        if tag in self.scene.tags:
            self.scene.tags[tag].append(self)
            self.tags.append(tag)

    def remove_tag(self, tag: str):
        if tag in self.scene.tags and self in self.scene.tags[tag]:
            self.scene.tags[tag].remove(self)
            self.tags.remove(tag)

    def has_tag(self, tag: str) -> bool:
        return tag in self.tags

    def add_component(
        self,
        component_type: type[Component],
        name: str = None,
        init_component: bool = True,
    ) -> Component:
        comp = component_type(self)
        if name is None:
            name = component_type.__name__

        if name in self._components:
            if self._components[name][0] is not None:
                self._components[name][1].append(self._components[name][0])
            self._components[name][1].append(comp)
            self._components[name][0] = None
        else:
            self._components[name] = [comp, []]

        if init_component:
            comp.init()
        return comp

    def get_component(self, name: str):
        if name in self._components:
            if self._components[name][0] is not None:
                return self._components[name][0]
            else:
                return self._components[name][1][0]
        return None

    def get_components(self, name: str):
        if name in self._components:
            if len(self._components[name][1]) > 1:
                return self._components[name][1]
            else:
                return [self._components[name][0]]
        return None

    def has_component(self, name: str):
        return name in self._components

    def destroy(self):
        self.on_destroy()
        for tag in list(self.tags):
            self.remove_tag(tag)
        for single, multiple in list(self._components.values()):
            if single is not None:
                single.on_destroy()
                single.destroy()
            else:
                for comp in multiple:
                    comp.on_destroy()
                    comp.destroy()
        for layer in list(self.layers.values()):
            layer.remove(self)
            
    def awake_components(self):
        for single, multiple in list(self._components.values()):
            if single is not None:
                single.awake()
            else:
                for comp in multiple:
                    comp.awake()
                    
    def update_components(self):
        self.box.center = self.transform.position
        self.box.size = (
            (
                self.texture.width * self.transform.scale.x,
                self.texture.height * self.transform.scale.y,
            )
            if self.texture is not None
            else self.box.size
        )
        for single, multiple in list(self._components.values()):
            if single is not None:
                single.update()
            else:
                for comp in multiple:
                    comp.update()
                    
    def event_components(self, event: pygame.event.Event):
        for single, multiple in list(self._components.values()):
            if single is not None:
                single.event(event)
            else:
                for comp in multiple:
                    comp.event(event)
                    
    def on_quit_components(self):
        for single, multiple in list(self._components.values()):
            if single is not None:
                single.on_quit()
            else:
                for comp in multiple:
                    comp.on_quit()

    # overridable
    @classmethod
    def instantiate(cls) -> Self:
        return cls(Transform(), [], None)

    def render(self):
        for single, multiple in list(self._components.values()):
            if single is not None:
                single.render()
            else:
                for comp in multiple:
                    comp.render()
                    
    def on_destroy(self):
        ...

    def init(self):
        ...
        
    def awake(self):
        ...
                    
    def update(self):
        ...
                    
    def event(self, event: pygame.event.Event):
        ...

    def on_quit(self):
        ...


class Layer:
    def __init__(
        self,
        name: str,
        is_main: bool = False,
        is_visible: bool = False,
        is_other: bool = False,
    ):
        self.name: str = name
        self.entities: list[Entity] = []
        self.is_main: bool = is_main
        self.is_visible: bool = is_visible
        self.is_other: bool = is_other

    def add(self, *entities: list[Entity]):
        for entity in entities:
            if entity in self.entities:
                continue
            entity.layers[self.name] = self
            self.entities.append(entity)

    def remove(self, *entities: list[Entity]):
        for entity in entities:
            if entity not in self.entities:
                continue
            del entity.layers[self.name]
            self.entities.remove(entity)

    def update(self):
        for entity in list(self.entities):
            entity.update()
            entity.update_components()

    def event(self, event: pygame.event.Event):
        for entity in list(self.entities):
            entity.event(event)
            entity.event_components(event)

    def sort(self, key: Callable[[Entity], bool]):
        self.entities = sorted(self.entities, key=key)

    def on_quit(self):
        for entity in list(self.entities):
            entity.on_quit()
            entity.on_quit_components()

    def empty(self):
        for entity in list(self.entities):
            entity.destroy()

    def render(self):
        for entity in list(self.entities):
            entity.render()
            
    def awake(self):
        for entity in list(self.entities):
            entity.awake_components()
            entity.awake()

    def draw(self):
        for entity in self.entities:
            if entity.texture is None:
                continue
            transform, texture = entity.transform, entity.texture
            size_x, size_y = int(texture.width * transform.scale.x), int(
                texture.height * transform.scale.y
            )
            texture.draw(
                dstrect=(
                    transform.position.x
                    - size_x // 2
                    - Camera.position.x
                    + Window.center.x,
                    transform.position.y
                    - size_y // 2
                    - Camera.position.y
                    + Window.center.y,
                    size_x,
                    size_y,
                ),
                angle=transform.rotation,
                flip_x=transform.flipx,
                flip_y=transform.flipy,
            )


class SceneConfig:
    def __init__(
        self,
        skybox_color: str = "black",
        visible_layer_names: list[str] = ["visible-main"],
        other_layer_names: list[str] = [],
        tags: list[str] = [],
    ):
        self.skybox_color: str = pygame.Color(skybox_color)
        self.visible_layer_names: list[str] = visible_layer_names
        self.other_layer_names: list[str] = other_layer_names
        self.tags: list[str] = tags


class Scene:
    def __init__(self, _id):
        self._id = _id + 1
        self._has_config: bool = False

    def config(self, config: SceneConfig):
        if self._has_config:
            return False
        self.skybox_color: str = config.skybox_color

        self.layers: dict[str, Layer] = {}
        self._visible_layers: dict[str, Layer] = {}
        self._other_layers: dict[str, Layer] = {}
        self._main_layers: dict[str, Layer] = {}
        for name in [
            "all",
            "updates",
            "event-handler",
            "quit-handler",
            "rendering",
            "ignore-cast",
        ]:
            layer = Layer(name, is_main=True)
            self.layers[name] = layer
            self._main_layers[name] = layer
        for name in config.visible_layer_names:
            layer = Layer(name, is_visible=True)
            self.layers[name] = layer
            self._visible_layers[name] = layer
        for name in config.other_layer_names:
            layer = Layer(name, is_other=True)
            self.layers[name] = layer
            self._other_layers[name] = layer

        self.tags: dict[str, list[Entity]] = {}
        for tag in config.tags:
            self.tags[tag] = []

        self._has_config = True
        return True

    def get_by_tag(self, tag: str) -> list[Entity]:
        return self.tags[tag]

    def update(self):
        self._main_layers["updates"].update()

    def event(self, event: pygame.event.Event):
        self._main_layers["event-handler"].event(event)

    def unload(self):
        for layer in list(self.layers.values()):
            layer.empty()
            del self.layers[layer.name]
        del self

    def draw(self):
        for layer in self._visible_layers.values():
            layer.draw()

    def on_quit(self):
        self._main_layers["all"].empty()
        self._main_layers["quit-handler"].on_quit()

    def render(self):
        self._main_layers["rendering"].render()
        
    def awake(self):
        self._main_layers["all"].awake()


class Scenes:
    scene: Scene = None
    scene_funcs: dict[str, Callable] = {}

    @classmethod
    def new_scene(cls, config: SceneConfig) -> Scene:
        old_id = 0
        if cls.scene:
            old_id = cls.scene._id
            cls.scene.unload()
        cls.scene = Scene(old_id)
        cls.scene.config(config)
        return cls.scene
    
    @classmethod
    def register_scene_func(cls, scene_func: Callable, name: str|None = None):
        if name is None:
            name = scene_func.__name__
        cls.scene_funcs[name] = scene_func
        
    @classmethod
    def register_scene_funcs(cls, *scene_funcs: Callable):
        for func in scene_funcs: cls.register_scene_func(func)
        
    @classmethod
    def get_scene_func(cls, name: str) -> Callable|None:
        return cls.scene_funcs.get(name, None)
    
    @classmethod
    def call_scene_func(cls, name: str) -> Callable|None:
        scene_func = cls.scene_funcs.get(name, None)
        if scene_func is not None:
            scene_func()
        return scene_func

import pygame
from .transform import Transform
from .components import Component
import pygame._sdl2 as pgsdl
from ..core.camera import Camera

class Entity:
    start_components = []
    instance = None
    unique = False

    def __init__(self, transform:Transform, layer_names:list[str], texture:pgsdl.Texture=None, tags:list[str]=None):
        # scene
        self.scene = Scenes.scene
        # transform
        self.transform = transform
        # layers
        self.layers:dict[str, Layer] = {}
        if not "all" in layer_names: layer_names.append("all")
        for layer in layer_names: self.scene.layers[layer].add(self)
        # name
        self.name = self.__class__.__name__
        # texture
        self.texture = texture
        # box
        self.box = pygame.Rect = self.texture.get_rect(center=self.transform.position)
        # tags
        self.tags = []
        tags = tags if tags is not None else []
        for tag in tags: self.add_tag(tag)
        # components
        self.components:dict[str, Component] = {}
        for comp in self.start_components:
            if isinstance(comp, list): comp_name, comp_type = comp
            else: comp_name, comp_type = comp.__name__, comp
            self.components[comp_name] = comp_type(self)
        for comp in list(self.components.values()): comp.init()
        # unique
        if self.unique:
            self.__class__.instance = self
            setattr(self.scene, self.__class__.__name__, self)
        # init
        self.init()

    # builtin
    def add_tag(self, tag:str):
        if tag in self.scene.tags:
            self.scene.tags[tag].append(self)
            self.tags.append(tag)

    def remove_tag(self, tag:str):
        if tag in self.scene.tags and self in self.scene.tags[tag]:
            self.scene.tags[tag].remove(self)
            self.tags.remove(tag)

    def has_tag(self, tag:str):
        return tag in self.tags

    def add_component(self, name:str, component_type:type[Component]):
        comp = component_type(self)
        self.components[name] = comp
        comp.init()
        return comp
    
    def destroy(self):
        for tag in list(self.tags): self.remove_tag(tag)
        for comp in list(self.components.values()): comp.on_destroy()
        for layer in list(self.layers.values()):
            layer.remove(self)
    
    # overridable
    @classmethod
    def instantiate(cls):
        return cls(Transform(), [], None)

    def render(self):
        for comp in list(self.components.values()): comp.render()

    def init(self): ...

    def update(self):
        for comp in list(self.components.values()): comp.update()

    def event(self, event):
        for comp in list(self.components.values()): comp.event(event)

    def on_quit(self):
        for comp in list(self.components.values()): comp.on_quit()

class Layer:
    def __init__(self, name):
        self.name = name
        self.entities:list[Entity] = []

    def add(self, *entities):
        for entity in entities:
            entity.layers[self.name] = self
            self.entities.append(entity)

    def remove(self, *entities):
        for entity in entities:
            del entity.layers[self.name]
            self.entities.remove(entity)
            
    def update(self):
        for entity in list(self.entities): entity.update()

    def event(self, event):
        for entity in list(self.entities): entity.event(event)

    def sort(self, key):
        self.entities = sorted(self.entities, key=key)

    def on_quit(self):
        for entity in list(self.entities): entity.on_quit()

    def empty(self):
        self.remove(*list(self.entities))

    def render(self):
        for entity in list(self.entities): entity.render()

    def draw(self):
        for entity in self.entities:
            if entity.texture is None: continue
            size_x, size_y = int(entity.texture.width*entity.transform.scale.x), int(entity.texture.height*entity.transform.scale.y)
            entity.texture.draw(dstrect=(entity.transform.position.x-size_x//2-Camera.position.x,
                                         entity.transform.position.y-size_y//2-Camera.position.y, size_x, size_y), 
                                angle=entity.transform.rotation,flip_x=entity.transform.flipx, flip_y=entity.transform.flipy)

class SceneConfig:
    def __init__(self, skybox_color="black", visible_layer_names = ["visible-main"], other_layer_names=[], tags=[]):
        self.skybox_color = pygame.Color(skybox_color)
        self.visible_layer_names = visible_layer_names
        self.other_layer_names = other_layer_names
        self.tags = tags

class Scene:
    def __init__(self):
        self.has_config = False

    def config(self, config:SceneConfig):
        if self.has_config: return False
        self.skybox_color = config.skybox_color

        self.layers:dict[str, Layer] = {}
        self.visible_layers:dict[str, Layer] = {}
        self.other_layers:dict[str, Layer] = {}
        self.main_layers:dict[str, Layer] = {}
        for name in ["all","updates","event-handler", "quit-handler", "rendering"]:
            layer = Layer(name)
            self.layers[name] = layer
            self.main_layers[name] = layer
        for name in config.visible_layer_names:
            layer = Layer(name)
            self.layers[name] = layer
            self.visible_layers[name] = layer
        for name in config.other_layer_names:
            layer = Layer(name)
            self.layers[name] = layer
            self.other_layers[name] = layer

        self.tags:dict[str,list[Entity]] = {}
        for tag in config.tags: self.tags[tag] = []

        self.has_config = True
        return True

    def get_by_tag(self, tag:str):
        return self.tags[tag]

    def update(self):
        self.main_layers["updates"].update()

    def event(self, event):
        self.main_layers["event-handler"].event(event)

    def unload(self):
        for layer in list(self.layers.values()): 
            layer.empty()
            del self.layers[layer.name]
        del self

    def draw(self):
        for layer in self.visible_layers.values():
            layer.draw()

    def on_quit(self):
        self.main_layers["quit-handler"].on_quit()

    def render(self):
        self.main_layers["rendering"].render()

class Scenes:
    scene: Scene = None

    @classmethod
    def new_scene(cls, config:SceneConfig):
        if cls.scene: cls.scene.unload()
        cls.scene = Scene()
        cls.scene.config(config)
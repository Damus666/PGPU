import json
import pygame


def load(path: str):
    with open(path, "r") as file:
        return json.load(file)


def save(data: dict, path: str):
    with open(path, "w") as file:
        json.dump(data, file)


def load_str(string:str):
    return json.loads(string)


def save_vec2(vec2: pygame.Vector2):
    return {"x": vec2.x, "y": vec2.y}


def save_vec3(vec3: pygame.Vector3):
    return {"x": vec3.x, "y": vec3.y, "z": vec3.z}


def load_vec2(vec2_json: dict[str, float]):
    return pygame.Vector2(*list(vec2_json.values()))


def load_vec3(vec3_json: dict[str, float]):
    return pygame.Vector3(*list(vec3_json.values()))


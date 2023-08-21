import json


def load(path: str):
    with open(path, "r") as file:
        return json.load(file)


def save(data: dict, path: str):
    with open(path, "w") as file:
        json.dump(data, file)

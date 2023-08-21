import json, os

class JSON:
    @staticmethod
    def load(path:str):
        with open(path, "r") as file:
            return json.load(file)
        
    @staticmethod
    def save(data:dict, path:str):
        with open(path, "w") as file:
            json.dump(data, file)

class File:
    @staticmethod
    def names(path:str):
        return [file_name.split(".")[0] for file_name in os.listdir(path) if "." in file_name]
    
    @staticmethod
    def names_full(path:str): return [name for name in os.listdir(path) if "." in name]

    @staticmethod
    def names_strict(path:str, exclude:list[str], extensions:list[str]):
        files = [file_name.split(".")[0] for file_name in os.listdir(path) if "." in file_name and file_name.split(".")[1] in extensions]
        for file in exclude:
            if file in files: files.remove(file)
        return files
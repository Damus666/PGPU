import os


def names(path: str) -> list[str]:
    return [
        file_name.split(".")[0] for file_name in os.listdir(path) if "." in file_name
    ]


def names_full(path: str) -> list[str]:
    return [name for name in os.listdir(path) if "." in name]


def names_strict(path: str, exclude: list[str], extensions: list[str]) -> list[str]:
    files = [
        file_name.split(".")[0]
        for file_name in os.listdir(path)
        if "." in file_name and file_name.split(".")[1] in extensions
    ]
    for file in exclude:
        if file in files:
            files.remove(file)
    return files


def empty_folder(
    folder_path: str, exclude: list[str] = None, extensions: list[str] = None
):
    for file_name in os.listdir(folder_path):
        if exclude is not None and file_name in exclude:
            continue
        if (
            extensions is not None
            and "." in file_name
            and file_name.split(".")[1] not in extensions
        ):
            continue
        if "." in file_name:
            os.remove(folder_path + "/" + file_name)

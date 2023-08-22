import pygame, os


class Sound:
    def __init__(self, sound: pygame.mixer.Sound, volume: float = 1, name: str = None):
        self.name: str = name if name is not None else "Unnamed Sound"
        self.sound: pygame.mixer.Sound = sound
        self.volume: float = pygame.math.clamp(volume, 0, 1)
        self.set_volume(1)

    def set_volume(self, master_volume: float = 1):
        self.sound.set_volume(pygame.math.clamp(master_volume * self.volume, 0, 1))

    def play(self, loops: int = 1, maxtime: int = 0, fade_ms: int = 0):
        self.sound.play(loops, maxtime, fade_ms)

    def stop(self):
        self.sound.stop()

    @property
    def length(self) -> float:
        return self.sound.get_length()

    @property
    def real_volume(self) -> float:
        return self.sound.get_volume()


class SoundCollection:
    def __init__(self, sounds: list[Sound] = None, volume: float = 1):
        self.sounds: dict[str, Sound] = {}
        self.volume: float = pygame.math.clamp(volume, 0, 1)
        sounds = [] if sounds is None else sounds
        for sound in sounds:
            self.sounds[sound.name] = sound

    def refresh_volumes(self):
        for sound in self.sounds.values():
            sound.set_volume(self.volume)

    def set_volume(self, volume: float = 1):
        self.volume = pygame.math.clamp(volume, 0, 1)
        self.refresh_volumes()

    def update_volume(self, amount: float):
        self.volume = pygame.math.clamp(self.volume + amount, 0, 1)
        self.refresh_volumes()

    def add_sound(self, sound: Sound):
        self.sounds[sound.name] = sound

    def add(self, sound: pygame.mixer.Sound, name: str, volume: float = 1) -> Sound:
        sound_asset = Sound(sound, volume, name)
        self.sounds[name] = sound_asset
        return sound_asset

    def __getitem__(self, name) -> Sound:
        return self.sounds[name]


class Music:
    global_volume: float = 1
    music_volume: float = 1

    @classmethod
    def set_volume(self, volume: float = 1):
        self.global_volume = pygame.math.clamp(volume, 0, 1)
        self.refresh_volumes()

    @classmethod
    def update_volume(self, amount: float):
        self.global_volume = pygame.math.clamp(self.global_volume + amount, 0, 1)
        self.refresh_volumes()

    @classmethod
    def refresh_volumes(self):
        pygame.mixer.music.set_volume(
            pygame.math.clamp(self.music_volume * self.global_volume, 0, 1)
        )

    @classmethod
    def load(self, path: str, music_volume: float = 1):
        pygame.mixer.music.unload()
        pygame.mixer.music.load(path)
        self.music_volume = pygame.math.clamp(music_volume, 0, 1)
        self.refresh_volumes()

    @classmethod
    def play(self, loops: int = 1, maxtime: int = 0, fade_ms: int = 0):
        pygame.mixer.music.play(loops, maxtime, fade_ms)

    @classmethod
    def load_play(
        self,
        path: str,
        music_volume: float = 1,
        loops: int = 1,
        maxtime: int = 0,
        fade_ms: int = 0,
    ):
        self.load(path, music_volume)
        self.play(loops, maxtime, fade_ms)

    @staticmethod
    def stop():
        pygame.mixer.music.stop()

    @staticmethod
    def pause():
        pygame.mixer.music.pause()

    @staticmethod
    def unpause():
        pygame.mixer.music.unpause()

    @staticmethod
    def rewind():
        pygame.mixer.music.rewind()


def load(path: str, volume: float = 1) -> pygame.mixer.Sound:
    sound = pygame.mixer.Sound(path)
    sound.set_volume(pygame.math.clamp(volume, 0, 1))
    return sound


def load_sound(path: str, volume: float = 1, name: str = None) -> Sound:
    return Sound(pygame.mixer.Sound(path), volume, name)


def load_list(
    folder_path: str, volume: float | list[float] | tuple[float, ...] = 1
) -> list[Sound]:
    sounds = []
    for i, name in enumerate(os.listdir(folder_path)):
        sound = pygame.mixer.Sound(folder_path + "/" + name)
        vol = volume[i] if isinstance(volume, (list, tuple)) else volume
        sound.set_volume(vol)
        sounds.append(sound)
    return sounds


def load_collection(
    folder_path: str,
    main_volume: float = 1,
    volumes: float | list[float] | tuple[float, ...] = 1,
) -> SoundCollection:
    collection = SoundCollection(volume=main_volume)
    for i, name in enumerate(os.listdir(folder_path)):
        sound = pygame.mixer.Sound(folder_path + "/" + name)
        vol = volumes[i] if isinstance(volumes, (list, tuple)) else volumes
        collection.add(sound, name.split(".")[0], vol)
    return collection

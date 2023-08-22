import pygame, time
from ..utils import classproperty
from typing import Callable


class Timer:
    def __init__(
        self, cooldown: int, callback: Callable = None, start_active: bool = True
    ):
        self.cooldown: int = cooldown
        self.callback: Callable = callback
        self.active: bool = False
        self._start_time: int = -1
        if start_active:
            self.activate()

    def activate(self):
        self.active = True
        self._start_time = Time.ticks

    def deactivate(self):
        self.active = False
        self._start_time = -1

    def update(self):
        if not self.active:
            return
        if Time.ticks - self._start_time >= self.cooldown:
            self.deactivate()
            if self.callback:
                self.callback()

    def has_finished(self) -> bool:
        return Time.ticks - self._start_time >= self.cooldown


class Time:
    delta_time: float = 0
    ticks: int = 0
    time: float = 0
    clock: pygame.Clock = None
    target_fps: float = 0
    framerate: float = 0
    time_scale: float = 1
    frame_count: int = 0

    _timers: dict[str, Timer] = dict()
    _invokes: list = []

    @classmethod
    def _init(cls, target_fps: float = 0):
        cls.target_fps = target_fps
        cls.clock = pygame.time.Clock()

    @classmethod
    def _update(cls):
        cls.delta_time = cls.clock.tick(cls.target_fps) * 0.001 * cls.time_scale
        cls.ticks = pygame.time.get_ticks()
        cls.time = cls.ticks * 0.001
        cls.framerate = cls.clock.get_fps()
        cls.frame_count += 1
        for timer in cls._timers.values():
            if timer._auto_update:
                timer.update()
        toremove = []
        for invoke in cls._invokes:
            if cls.ticks - invoke[2] >= invoke[1]:
                invoke[0]()
                toremove.append(invoke)
        for el in toremove:
            cls._invokes.remove(el)

    @staticmethod
    def delay(milliseconds: int) -> int:
        return pygame.time.delay(milliseconds)

    @classmethod
    def invoke(cls, function: Callable, time_ms: int, name: str = None):
        cls._invokes.append((function, time_ms, cls.ticks, name))

    @classmethod
    def clear_invokes(cls):
        cls._invokes.clear()

    @classmethod
    def stop_invoke(cls, name):
        for invoke in list(cls._invokes):
            if invoke[-1] == name:
                cls._invokes.remove(invoke)

    @classmethod
    def add_timer(
        cls,
        name: str,
        cooldown: int,
        callback: Callable = None,
        start_active: bool = True,
        auto_update: bool = True,
    ) -> Timer:
        cls._timers[name] = (new_timer := Timer(cooldown, callback))
        if start_active:
            new_timer.activate()
        new_timer._auto_update = auto_update
        return new_timer

    @classmethod
    def get_timer(cls, name: str) -> Timer:
        return cls._timers[name]

    @classmethod
    def activate_timer(cls, name: str):
        cls._timers[name].activate()

    @classmethod
    def deactivate_timer(cls, name: str):
        cls._timers[name].deactivate()

    @classmethod
    def has_timer_finished(cls, name: str) -> bool:
        return cls._timers[name].has_finished()

    @classmethod
    def get_timers(cls):
        return cls._timers.values()

    @classproperty
    def systime(cls):
        return time.time()

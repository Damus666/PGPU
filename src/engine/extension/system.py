import psutil, sys, pygame
from ..utils import classproperty

class System:
    process: psutil.Process = None

    @classmethod
    def _init(cls): cls.process = psutil.Process()

    @staticmethod
    def exit(code:str): sys.exit(code)

    @staticmethod
    def process_iter(): return psutil.process_iter()

    @staticmethod
    def pid_exists(pid:int): return psutil.pid_exists(pid)

    @staticmethod
    def disk_usage(path:str): return psutil.disk_usage(path)

    @classproperty
    def disk_partitions(cls): return psutil.disk_partitions()

    @classproperty
    def global_cpu_data(cls): return {
        "count": psutil.cpu_count(),
        "freq": psutil.cpu_freq(),
        "percent": psutil.cpu_percent(),
        "times": psutil.cpu_times(),
    }

    @classproperty
    def total_cpu_usage(cls): return psutil.cpu_percent()

    @classproperty
    def pids(cls): return psutil.pids()

    @classproperty
    def total_ram(cls): return pygame.system.get_total_ram()
    
    @classproperty
    def screens_resolution(cls): return pygame.display.get_desktop_sizes()
    
    @classproperty
    def screen_resolution(cls): return pygame.display.get_desktop_sizes()[0]
    
    @classproperty
    def refresh_rate(cls): return pygame.display.get_current_refresh_rate()
    
    @classproperty
    def num_displays(cls): return pygame.display.get_num_displays()
    
    @classproperty
    def screen_refresh_rates(cls): return pygame.display.get_desktop_refresh_rates()
    
    @classproperty
    def screen_refresh_rate(cls): return pygame.display.get_desktop_refresh_rate()
import psutil, sys, pygame, screeninfo


def exit(code: str):
    sys.exit(code)


def disk_usage(path: str):
    return psutil.disk_usage(path)


def global_cpu_data():
    return {
        "count": psutil.cpu_count(),
        "freq": psutil.cpu_freq(),
        "percent": psutil.cpu_percent(),
        "times": psutil.cpu_times(),
    }


def total_cpu_usage():
    return psutil.cpu_percent()


def total_ram():
    return pygame.system.get_total_ram()


def pids():
    return psutil.pids()


def pid_exists(pid: int):
    return psutil.pid_exists(pid)


def process_iter():
    return psutil.process_iter()

def new_process(pid: int = None):
    return psutil.Process(pid)


PROCESS: psutil.Process = psutil.Process()
DISK_PARTITIONS:list[psutil._common.sdiskpart] = psutil.disk_partitions()
ALL_DISK_PARTITIONS:list[psutil._common.sdiskpart] = psutil.disk_partitions(True)

MONITORS:list[screeninfo.Monitor] = screeninfo.get_monitors()
PRIMARY_MONITOR:screeninfo.Monitor
for monitor in MONITORS:
    if monitor.is_primary: PRIMARY_MONITOR = monitor
SCREEN_RESOLUTION = pygame.Vector2(PRIMARY_MONITOR.width, PRIMARY_MONITOR.height)

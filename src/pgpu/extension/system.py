import psutil, sys, pygame


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


def get_process():
    return process


def new_process(pid: int = None):
    return psutil.Process(pid)


process: psutil.Process = psutil.Process()
DISK_PARTITIONS = psutil.disk_partitions()
ALL_DISK_PARTITIONS = psutil.disk_partitions(True)

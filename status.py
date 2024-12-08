import psutil

def get_status_info() -> dict:
    memory = psutil.virtual_memory()

    ram_usage: float = memory.used / (1024 ** 2)
    ram_total: float = memory.total / (1024 ** 2)

    disk = psutil.disk_usage('/')
    disk_usage: float = disk.used / (1024 ** 2)
    disk_total: float = disk.total / (1024 ** 2)

    cpu_usage: float = psutil.cpu_percent(interval=1)

    return {
        "disk_total": disk_total,
        "disk_usage": disk_usage,
        "ram_total": ram_total,
        "ram_usage": ram_usage,
        "cpu_usage": cpu_usage
    }

if __name__ == "__main__":
    print(get_status_info())

    
import asyncio
import platform

from core.camera import capture_image
from core.storage import generate_filename


def handle_wakeup():

    path = generate_filename()

    if capture_image(str(path)):
        print("Captured:", path)

    else:
        print("Capture failed")


def get_listener():

    system = platform.system()

    if system == "Linux":
        from platforms.linux import LinuxWakeListener
        return LinuxWakeListener()

    elif system == "Windows":
        from platforms.windows import WindowsWakeListener
        return WindowsWakeListener()

    else:
        raise NotImplementedError(
            f"Unsupported OS: {system}"
        )


async def async_main():

    listener = get_listener()

    await listener.start(handle_wakeup)


def sync_main():

    listener = get_listener()

    listener.start(handle_wakeup)


if __name__ == "__main__":

    if platform.system() == "Linux":
        asyncio.run(async_main())

    elif platform.system() == "Windows":
        sync_main()
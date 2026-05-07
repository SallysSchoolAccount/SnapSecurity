import asyncio

from platforms.linux import LinuxWakeListener
from core.camera import capture_image
from core.storage import generate_filename


def handle_wakeup():

    path = generate_filename()

    if capture_image(str(path)):
        print("Captured:", path)
    else:
        print("Capture failed")


async def main():

    listener = LinuxWakeListener()

    await listener.start(handle_wakeup)


asyncio.run(main())
from dbus_next.aio import MessageBus
from dbus_next.constants import BusType
import asyncio

class LinuxWakeListener:
    async def start(self, callback):
        bus = await MessageBus(
            bus_type=BusType.SYSTEM
        ).connect()

        introspection = await bus.introspect(
            'org.freedesktop.login1',
            '/org/freedesktop/login1'
        )

        obj = bus.get_proxy_object(
            'org.freedesktop.login1',
            '/org/freedesktop/login1',
            introspection
        )

        manager = obj.get_interface(
            'org.freedesktop.login1.Manager'
        )

        def on_prepare_for_sleep(is_sleep: bool):
            print("Sleep event: ", is_sleep)

            if not is_sleep:
                callback()

        manager.on_prepare_for_sleep(
            on_prepare_for_sleep
        )

        print("Listening for sleep events...")
        await asyncio.Event().wait()
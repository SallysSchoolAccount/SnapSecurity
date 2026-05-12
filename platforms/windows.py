import ctypes
from ctypes import wintypes

import win32con
import win32gui

DEVICE_NOTIFY_WINDOW_HANDLE = 0x00000000

PBT_APMRESUME = 0x0007
PBT_APMRESUMEAUTOMATIC = getattr(win32con, "PBT_APMRESUMEAUTOMATIC", 0x0012)


class WindowsWakeListener:

    def __init__(self):
        self.callback = None
        self.hwnd = None
        self._notify_handle = None

    def start(self, callback):

        self.callback = callback

        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self.wndproc
        wc.lpszClassName = "WakeSentinelWindow"

        class_atom = win32gui.RegisterClass(wc)

        self.hwnd = win32gui.CreateWindow(
            class_atom,
            "WakeSentinel",
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            None
        )

        user32 = ctypes.windll.user32
        user32.RegisterSuspendResumeNotification.restype = wintypes.HANDLE
        user32.RegisterSuspendResumeNotification.argtypes = [
            wintypes.HANDLE,
            wintypes.DWORD
        ]

        self._notify_handle = user32.RegisterSuspendResumeNotification(
            wintypes.HANDLE(self.hwnd),
            DEVICE_NOTIFY_WINDOW_HANDLE
        )

        if not self._notify_handle:
            print("Warning: Failed to register for suspend/resume notifications")
        else:
            print("Registered for suspend/resume notifications")

        print("Listening for Windows power events...")
        win32gui.PumpMessages()

    def wndproc(self, hwnd, msg, wparam, lparam):

        if msg == win32con.WM_POWERBROADCAST:

            print("Power event:", wparam)

            if wparam == PBT_APMRESUMEAUTOMATIC or wparam == PBT_APMRESUME:
                print("System resumed from sleep")

                if self.callback:
                    self.callback()

        return win32gui.DefWindowProc(
            hwnd,
            msg,
            wparam,
            lparam
        )
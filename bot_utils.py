import os
import re
from ctypes import windll
from ctypes import create_unicode_buffer

from utils import get_songs_path


windll.user32.SetProcessDPIAware()


def get_screen_res():
    return (
        windll.user32.GetSystemMetrics(0),
        windll.user32.GetSystemMetrics(1)
    )


def get_window():
    hwnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hwnd) + 1
    buffer = create_unicode_buffer(length)
    windll.user32.GetWindowTextW(hwnd, buffer, length)

    return buffer.value if buffer.value else ''


def move_cursor(x, y):
    windll.user32.SetCursorPos(int(x), int(y))


def shift_is_pressed(key):
    key_state = windll.user32.GetAsyncKeyState(
        windll.user32.VkKeyScanW(ord(key))
    ) & 0x8000 != 0

    shift_state = windll.user32.GetAsyncKeyState(0x10) & 0x8000 != 0
    
    return key_state and shift_state

def get_map_data(title):
    title = re.sub(r'[\\/:*?"<>|]', '', title)
    start = title.find('-') + 2
    end = title.rfind('[')

    map_filename = title[start:end - 1]
    diff = title[end + 1:-1]

    return (
        map_filename,
        diff
    )


def get_map_file(name, diff):
    """
    Because some beatmap folders actually have multiple different songs (like jump training maps),
    it is actually necessary to look for every single .osu file inside each folder, instead
    of relying solely on the folder's name.
    """
    beatmap = None
    songs_path = get_songs_path()

    for entry in os.scandir(songs_path):
        if not entry.is_dir():
            continue

        for file in os.scandir(os.path.join(songs_path, entry.name)):
            file_name = file.name.lower()
            if file.is_file() and file_name.startswith(name.lower()) and file_name.endswith(f'[{diff.lower()}].osu'):
                beatmap = file
                break
        
        if beatmap is not None:
            with open(beatmap, 'r', encoding='utf8') as f:
                return f.readlines()

    return None

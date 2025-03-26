import os
import json
import tkinter as tk
from ctypes import windll
from tkinter import filedialog


SONGS_PATH = None
BEZIER_COEFFICIENT = None
SPINNER_MS_STEP = None


def is_first_time():
    if os.path.exists('./settings.json'):
        return False
    return True


def setup_first_time():
    songs_path = rf"{os.getenv('LOCALAPPDATA')}/osu!/Songs"

    if not os.path.exists(songs_path):
        pop_up_message(
            "Select Osu!'s Songs folder",
            "It looks like your Osu!'s Songs folder isn't at the default directory.\n" + \
            "Please, select it manually."
        )
        songs_path = ask_songs_path()

    settings = {
        'songs_path': songs_path.replace('\\', '/'),
        'bezier_coefficient': 0.01,
        'spinner_ms_step': 10,
        'description': "Higher values = faster loading time = worse bot performance, and vice-versa. 0.001 <= bezier_coefficient <= 0.1, 1 <= spinner_ms_step <= 100."
    }

    with open('./settings.json', 'w', encoding='utf8') as f:
        json.dump(settings, f, indent=4)

    load_settings()


def first_time_how_to_use_warning():
    pop_up_message(
        "IMPORTANT: How to use the bot",
        "Follow the instructions in the terminal for hotkeys usage.\n\n" + \
        "When pressing Shift+P to start the bot, make sure to be the most precise possible.\n\n" + \
        "If you don't sync the first object (circle, slider or spinner) well, the bot will be offsync."
    )   


def songs_path_exist():
    load_settings()

    if os.path.exists(SONGS_PATH):
        return True
    return False


def setup_songs_path_again():
    global SONGS_PATH

    pop_up_message(
        "Select Osu!'s Songs folder",
        "It looks like you moved your Osu!'s Songs folder.\n" + \
        "Please, select it again."
    )

    songs_path = ask_songs_path()

    with open('./settings.json', 'r+', encoding='utf8') as f:
        settings = {**json.load(f)}
        settings['songs_path'] = songs_path
        
        f.seek(0)
        json.dump(settings, f, indent=4)
        f.truncate()

    SONGS_PATH = songs_path


def pop_up_message(title, message):
    print("Read the pop-up message and press 'ok'.")
    windll.user32.MessageBoxW(0, message, title, 0)
    os.system('cls||clear')


def ask_songs_path():
    root = tk.Tk()
    root.withdraw()
    
    while True:
        songs_path = filedialog.askdirectory(title="Select Osu!'s Songs folder.") 
        
        if not songs_path:
            pop_up_message("Closing", "No folder was selected.")
            exit()
        elif not songs_path.endswith('/osu!/Songs'):
            pop_up_message("Invalid folder", "Folder's path should end with '/osu!/Songs'.")
        else:
            break

    return songs_path


def is_numeric(val):
    try:
        val = float(val)
    except ValueError:
        return False
    return val


def load_settings():
    global SONGS_PATH
    global BEZIER_COEFFICIENT
    global SPINNER_MS_STEP

    with open('./settings.json', 'r', encoding='utf8') as f:
        file = json.load(f)

    SONGS_PATH = file.get('songs_path')
    BEZIER_COEFFICIENT = file.get('bezier_coefficient')
    SPINNER_MS_STEP = file.get('spinner_ms_step')

    if SONGS_PATH is None or BEZIER_COEFFICIENT is None or SPINNER_MS_STEP is None:
        pop_up_message(
            'Missing setting in settings file',
            'Please, do not completely remove values from the settings file.\n' +
            "If you don't remember the value, delete the `settings.json` file for re-setup.`"
        )
        exit()
    if not is_numeric(BEZIER_COEFFICIENT) or not is_numeric(SPINNER_MS_STEP):
        pop_up_message(
            'Invalid value',
            "Either 'bezier_coeffiecient' or 'spinner_ms_step' have a non-numeric value.\n" +
            "If you don't remember the value, delete the `settings.json` file for re-setup.`"
        )
        exit()


def get_songs_path():
    return SONGS_PATH


def get_bezier_coefficient():
    return BEZIER_COEFFICIENT


def get_spinner_ms_step():
    return SPINNER_MS_STEP

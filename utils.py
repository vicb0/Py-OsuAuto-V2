import os
import json
import tkinter as tk
from ctypes import windll
from tkinter import filedialog


SONGS_PATH = None


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

    save_songs_path(songs_path)


def first_time_how_to_use_warning():
    pop_up_message(
        "IMPORTANT: How to use the bot",
        "Follow the instructions in the terminal for hotkeys usage.\n" + \
        "When pressing Shift+P to start the bot, make sure to be the most precise possible.\n" + \
        "If you don't sync the first object (circle, slider or spinner) well, the bot will be offsync."
    )


def save_songs_path(songs_path):
    settings = {
        'songs_path': songs_path.replace('\\', '/')
    }

    with open('./settings.json', 'w', encoding='utf8') as f:
        json.dump(settings, f)


def songs_path_exist():
    with open('./settings.json', 'r', encoding='utf8') as f:
        path = json.load(f)['songs_path']

        if os.path.exists(path):
            return True
        return False


def setup_songs_path_again():
    pop_up_message(
        "Select Osu!'s Songs folder",
        "It looks like you moved your Osu!'s Songs folder.\n" + \
        "Please, select it again."
    )

    songs_path = ask_songs_path()
    save_songs_path(songs_path)


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


def load_songs_path():
    global SONGS_PATH

    with open('./settings.json', 'r', encoding='utf8') as f:
        SONGS_PATH = json.load(f)['songs_path']


def get_songs_path():
    return SONGS_PATH

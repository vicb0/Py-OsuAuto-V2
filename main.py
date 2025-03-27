from time import sleep

import utils
import parser
import bot_utils
from objects.Bot import Bot
from objects.Metadata import Metadata
from objects.HitObjectManager import HitObjectManager
from objects.TimingPointManager import TimingPointManager


def main():
    if utils.is_first_time():
        utils.setup_first_time()
        utils.first_time_how_to_use_warning()
    elif not utils.songs_path_exist():
        utils.setup_songs_path_again()

    print('=' * 50)
    print('ENABLE RELAX MOD')
    print('If the bot is taking too long to load maps in your machine, check the `settings.json` file.')
    print('=' * 50)
    print('Press Shift + one of the following keys:')
    print(">'D' to enable DT.\n>'H' to enable HT\n>'R' to enable HR.\n>'E' to enable EZ.")
    print("You can't toggle these while in a map.\n")

    while True:
        sleep(.1)

        if bot_utils.shift_is_pressed('d'):
            Metadata.toggle_DT()
            print(f"DT {'on' if Metadata.double_time else 'off'}.")
        elif bot_utils.shift_is_pressed('h'):
            Metadata.toggle_HT()
            print(f"HT {'on' if Metadata.half_time else 'off'}.")
        elif bot_utils.shift_is_pressed('r'):
            Metadata.toggle_HR()
            print(f"HR {'on' if Metadata.hard_rock else 'off'}.")
        elif bot_utils.shift_is_pressed('e'):
            Metadata.toggle_EZ()
            print(f"EZ {'on' if Metadata.easy else 'off'}.")

        window_title = bot_utils.get_window()

        if not window_title.startswith('osu! ') or not window_title.endswith(']'):
            continue

        name, diff = bot_utils.get_map_data(window_title)
        file = bot_utils.get_map_file(name, diff)

        if file is None:
            print('Could not find beatmap file.')
            continue

        Bot.reset_all()

        print('Parsing beatmap file...')
        parser.parse(file)

        if len(HitObjectManager.hos) == 0:
            print('Beatmap empty. Cancelled.\n')
            continue

        print('Doing math stuff... Pause the game while this is loading')
        Bot.setup()

        print("Ready! Press Shift+P to start and Shift+S to anytime to stop.")
        while not bot_utils.shift_is_pressed('p'):
            window_title = bot_utils.get_window()
            if window_title == 'osu!':
                print('Cancelled.')
                break
        else:
            Bot.play()
        print()


if __name__ == "__main__":
    main()

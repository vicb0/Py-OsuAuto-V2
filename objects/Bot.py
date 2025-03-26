from math import dist
from time import perf_counter

import bot_utils
from objects.Metadata import Metadata
from objects.PlayArea import PlayArea
from objects.BezierSlider import BezierSlider
from objects.TimingPointManager import TimingPointManager
from objects.HitObjectManager import HitObjectManager


class Bot:
    path = []
    idx = 0

    @staticmethod
    def reset_all():
        TimingPointManager.reset()
        HitObjectManager.reset()
        Bot.path.clear()
        Bot.idx = 0

    @staticmethod
    def next_point():
        Bot.idx += 1

    @staticmethod
    def get(offset=0):
        return Bot.path[Bot.idx + offset]

    @staticmethod
    def is_inbound(offset=0):
        return Bot.idx + offset < len(Bot.path)

    @staticmethod
    def calc_game():
        for c, ho in enumerate(HitObjectManager.hos):
            if c != 0:
                n = len(Bot.path) - 1
                last = Bot.path[n]

                while n >= 0 and last.offset >= ho.point.offset:
                    n -= 1
                    last = Bot.path[n]                    

                length = dist((last.x, last.y), (ho.point.x, ho.point.y))
                duration = ho.point.offset - last.offset

                path = BezierSlider.calc_bezier_curve(
                    [[(last.x, last.y), (ho.point.x, ho.point.y)]],
                    length,
                    duration,
                    last.offset
                )

                Bot.path.extend(path)

            if ho.object_type == 1:
                Bot.path.append(ho.point)
            else:
                Bot.path.extend(ho.path)
        
        Bot.path.sort(key=lambda x: x.offset)

    @staticmethod
    def convert_coords():
        for point in Bot.path:
            point.to_screen_point()

    @staticmethod
    def setup():
        # Gets screen resolution and playfield offset before the map starts
        # because maybe the player has a different ingame resolution than native,
        # so grabbing such informations when the bot launches might result in 
        # having the wrong resolution.
        PlayArea.calc_offsets()
        Metadata.calc_data()

        HitObjectManager.calc_slider_paths()
        HitObjectManager.calc_spinners()
        HitObjectManager.fix_stacks()

        Bot.calc_game()
        Bot.convert_coords()

    @staticmethod
    def play():
        first_offset = Bot.path[0].offset
        start = perf_counter()

        while Bot.is_inbound() and not bot_utils.shift_is_pressed('s'):
            current = Bot.get()

            if (perf_counter() - start) * 1000 >= current.offset - first_offset:
                bot_utils.move_cursor(current.x, current.y)
                Bot.next_point()

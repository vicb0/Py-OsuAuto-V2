import bot_utils


class PlayArea:
    width = 512
    height = 384

    start_x = None
    start_y = None
    scale = None

    @staticmethod
    def calc_offsets():
        x, y = bot_utils.get_screen_res()

        play_height = 0.8 * y
        play_width = (4 / 3) * play_height

        PlayArea.scale = play_height / 384

        # The playfield y position is offset down by 2% of the playfield height 
        PlayArea.start_y = (y - play_height) / 2 + 0.02 * play_height
        PlayArea.start_x = (x - play_width) / 2

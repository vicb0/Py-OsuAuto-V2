from objects.PlayArea import PlayArea


class Point:
    def __init__(self, x, y, offset):
        self.x = x
        self.y = y
        self.offset = offset

    def to_screen_point(self):
        self.x = PlayArea.start_x + self.x * PlayArea.scale
        self.y = PlayArea.start_y + self.y * PlayArea.scale

    def get_point(self):
        return (self.x, self.y)

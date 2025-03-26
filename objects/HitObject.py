from objects.Point import Point


class HitObject:
    def __init__(self, x, y, offset):
        self.point = Point(x, y, offset)
        self.stack_id = 0

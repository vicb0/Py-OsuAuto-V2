from math import pi
from math import sin
from math import cos

from objects.Point import Point
from objects.PlayArea import PlayArea
from objects.HitObject import HitObject


class Spinner(HitObject):
    rpm = 480
    radius = 0.05 * PlayArea.height
    millisecond_step = 10

    def __init__(self, offset, end):
        super().__init__(
            PlayArea.width / 2 + Spinner.radius,
            PlayArea.height / 2,
            offset
        )

        self.path = []
        self.end = end

        self.object_type = 3

    def stack(self):
        pass

    def calc_path(self):
        angle = 0
        radian = (Spinner.rpm / 60 / 1000 * 360) * pi / 180 * Spinner.millisecond_step
        offset = self.point.offset

        while offset < self.end:
            x = PlayArea.width / 2 + cos(angle) * Spinner.radius
            y = self.point.y + sin(angle) * Spinner.radius

            self.path.append(
                Point(
                    x, y,
                    offset
                )
            )

            offset += Spinner.millisecond_step
            angle = (angle + radian) % (2 * pi)

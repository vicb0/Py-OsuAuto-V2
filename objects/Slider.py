from objects.Point import Point
from objects.Metadata import Metadata
from objects.PlayArea import PlayArea
from objects.HitObject import HitObject
from objects.TimingPointManager import TimingPointManager


class Slider(HitObject):
    def __init__(self, x, y, offset, points, repeat, length):
        super().__init__(x, y, offset)
        self.points = points
        self.repeat = repeat
        self.length = length

        self.path = []
        self.sections = []
        self.duration = None
        self.object_type = 2

    def stack(self):
        self.point.x -= self.stack_id * Metadata.stack_offset
        self.point.y -= self.stack_id * Metadata.stack_offset

        for point in self.path:
            point.x -= self.stack_id * Metadata.stack_offset
            point.y -= self.stack_id * Metadata.stack_offset

    def calc_duration(self):
        self.duration = self.length / \
            (100 * Metadata.slider_multiplier * TimingPointManager.get().slider_vel) * \
            TimingPointManager.get().beat_dur

    def get_sections(self):
        temp = [[self.point.x, self.point.y]]
        tempc = 1

        for i in range(len(self.points)):
            point = self.points[i]

            if Metadata.hard_rock:
                point[1] = PlayArea.height - point[1]

            if point == temp[tempc - 1]:
                self.sections.append(temp)
                temp = [point]
                tempc = 1
            else:
                temp.append(point)
                tempc += 1

                if i == len(self.points) - 1:
                    self.sections.append(temp)

    def calc_repeats(self):
        whole_path = []

        for i in range(self.repeat - 1):
            curr_path = []

            if i % 2 == 0:
                step = range(len(self.path) - 1, -1, -1)
            else:
                step = range(0, len(self.path))

            for c, j in enumerate(step):
                curr_path.append(
                    Point(
                        self.path[j].x,
                        self.path[j].y,
                        self.path[c].offset + self.duration * (i + 1)
                    )
                )

            whole_path.extend(curr_path)

        self.path.extend(whole_path)

from objects.Metadata import Metadata

from objects.TimingPoint import TimingPoint
from objects.TimingPointManager import TimingPointManager

from objects.Circle import Circle
from objects.Spinner import Spinner
from objects.PlayArea import PlayArea
from objects.BezierSlider import BezierSlider
from objects.PerfectSlider import PerfectSlider
from objects.HitObjectManager import HitObjectManager


def parse_tps(file, line_idx):
    c = Metadata.speed_const

    line_idx += 1
    while line_idx < len(file):
        line = file[line_idx].strip()
        line_idx += 1

        if line == '':
            continue
        if line[0] == '[':
            line_idx -= 2
            break

        line = line.split(",")
        offset = float(line[0]) * c
        mult = float(line[1])

        if mult >= 0:
            vel = 1
            last_positive = mult * c
        else:
            vel = -100 / mult

        TimingPointManager.add(
            TimingPoint(
                offset,
                vel,
                last_positive
            )
        )

    return line_idx


def parse_hos(file, line_idx):
    spinner_types = {8, 12, 24, 28, 40, 44, 72, 76}
    c = Metadata.speed_const

    line_idx += 1
    while line_idx < len(file):
        line = file[line_idx].strip()
        line_idx += 1

        if line == '':
            continue
        if line[0] == '[':
            break

        line = line.split(',')
        x = int(line[0])
        y = int(line[1])

        if Metadata.hard_rock:
            y = PlayArea.height - y

        offset = int(line[2]) * c
        type_ = int(line[3])

        if type_ % 2 != 0:
            obj = Circle(
                x,
                y,
                offset
            )
        elif type_ in spinner_types:
            end = int(line[5]) * c

            obj = Spinner(
                offset,
                end,
            )
        else:
            kind, *points = line[5].split('|')
            points = [point.split(':') for point in points]
            points = [[int(x), int(y)] for x, y in points]
            repeats = int(line[6])
            length = float(line[7])

            params = (
                x,
                y,
                offset,
                points,
                repeats,
                length 
            )

            if kind in ('L', 'B'):
                obj = BezierSlider(*params)
            else:
                obj = PerfectSlider(*params)

        HitObjectManager.add(obj)


def parse(file):
    line_idx = 0
    hos_line_start = 0
    while line_idx < len(file):
        line = file[line_idx].strip()

        splitted = line.split(':')
        if len(splitted) == 2:
            _, value = splitted

        if line.startswith('StackLeniency'):
            Metadata.set_SL(value)
        elif line.startswith('CircleSize'):
            Metadata.set_CS(value)
        elif line.startswith('ApproachRate'):
            Metadata.set_AR(value)
        elif line.startswith('SliderMultiplier'):
            Metadata.set_SM(value)
        elif line.startswith('[TimingPoints]'):
            line_idx = parse_tps(file, line_idx)
        elif line.startswith('[HitObjects]'):
            hos_line_start = line_idx

        line_idx += 1

    parse_hos(file, hos_line_start)

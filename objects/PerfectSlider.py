from math import pi
from math import sin
from math import cos
from math import ceil
from math import sqrt
from math import acos
from math import dist
from math import atan2

from objects.Point import Point
from objects.Slider import Slider
from objects.BezierSlider import BezierSlider


class PerfectSlider(Slider):
    def __init__(self, x, y, offset, points, repeat, length):
        super().__init__(x, y, offset, points, repeat, length)

    def calc_path(self):
        self.path.extend(
            PerfectSlider.calc_curve(
                self.sections,
                self.length,
                self.duration,
                self.point.offset
            )
        )

    @staticmethod
    def calc_curve(sections, length, duration, offset):
        # Thanks to https://github.com/CookieHoodie/OsuBot/blob/master/OsuBots/OsuBot.cpp
        path = []
        pA, pB, pC = sections[0]

        try:
            center = PerfectSlider.find_center(pA, pB, pC)
        except ZeroDivisionError:
            return BezierSlider.calc_bezier_curve([[pA, pB, pC]], length, duration, offset)

        direction = PerfectSlider.calc_direction(pA, pB, pC)

        aSq = pow(pB[0] - pC[0], 2) + pow(pB[1] - pC[1], 2)
        bSq = pow(pA[0] - pC[0], 2) + pow(pA[1] - pC[1], 2)
        cSq = pow(pA[0] - pB[0], 2) + pow(pA[1] - pB[1], 2)

        linear_distance = sqrt(bSq)
        circle_distance = sqrt(aSq) + sqrt(cSq)

        if abs(linear_distance - circle_distance) < 0.01:
            return BezierSlider.calc_bezier_curve([[pA, pB, pC]], length, duration, offset)

        radius = dist(center, pA)

        dist_pA_center_x = pA[0] - center[0]
        dist_pA_center_y = pA[1] - center[1]

        dist_pC_center_x = pC[0] - center[0]
        dist_pC_center_y = pC[1] - center[1]

        ang_start = atan2(dist_pA_center_y, dist_pA_center_x)
        ang_end = atan2(dist_pC_center_y, dist_pC_center_x)

        while ang_start > ang_end:
            ang_end += 2 * pi

        ang_range = ang_end - ang_start

        if (direction < 0):
            ang_range = 2 * pi - ang_range

        points = max(2, ceil(ang_range / (2 * acos(1 - 0.01 / radius))))

        for i in range(points):
            fract = i / (points - 1)
            increment = direction * fract * ang_range
            ang = ang_start + increment

            x = center[0] + radius * cos(ang)
            y = center[1] + radius * sin(ang)

            path.append(
                Point(
                    x, y,
                    offset + (abs(increment * radius) / length) * duration
                )
            )

            if abs(increment * radius) >= length:
                break

        return path
    
    @staticmethod
    def find_center(A, B, C):
        x12 = A[0] - B[0]
        x13 = A[0] - C[0]
    
        y12 = A[1] - B[1]
        y13 = A[1] - C[1]
    
        y31 = C[1] - A[1]
        y21 = B[1] - A[1]
    
        x31 = C[0] - A[0]
        x21 = B[0] - A[0]

        sx13 = pow(A[0], 2) - pow(C[0], 2); 
        sy13 = pow(A[1], 2) - pow(C[1], 2); 
        sx21 = pow(B[0], 2) - pow(A[0], 2); 
        sy21 = pow(B[1], 2) - pow(A[1], 2); 

        f = ((sx13) * (x12) \
            + (sy13) * (x12) \
            + (sx21) * (x13) \
            + (sy21) * (x13)) \
            / (2 * ((y31) * (x12) - (y21) * (x13)))
        g = ((sx13) * (y12) \
            + (sy13) * (y12) \
            + (sx21) * (y13) \
            + (sy21) * (y13)) \
            / (2 * ((x31) * (y12) - (x21) * (y13)))
    
        c = -pow(A[0], 2) - pow(A[1], 2) - 2 * g * A[0] - 2 * f * A[1]

        return (-g, -f)

    @staticmethod
    def calc_direction(pA, pB, pC):
        s = (pB[0] - pA[0]) * (pC[1] - pA[1]) - (pC[0] - pA[0]) * (pB[1] - pA[1])

        if (s > 0): # clockwise
            return 1
        elif (s < 0): # counter clockwise
            return -1
        else: # colinear
            return 0

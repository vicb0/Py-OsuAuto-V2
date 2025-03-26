from math import dist

from objects.Point import Point
from objects.Slider import Slider
from utils import get_bezier_coefficient


class BezierSlider(Slider):
    coefficient = None

    def __init__(self, x, y, offset, points, repeat, length):
        super().__init__(x, y, offset, points, repeat, length)

    def calc_path(self):
        self.path.extend(
            BezierSlider.calc_bezier_curve(
                self.sections,
                self.length,
                self.duration,
                self.point.offset
            )
        )

    @staticmethod
    def calc_bezier_curve(sections, length, duration, offset):
        # Thanks to https://osu.ppy.sh/community/forums/topics/606522
        path = []
        dist_to_last = 0
        total_distance = 0
        point = sections[0][0]
        t = BezierSlider.coefficient

        min_dist = length / (1 / t)

        for section in sections:
            t_aux = 0

            while t_aux <= 1 and total_distance < length:
                bezierX = 0
                bezierY = 0
                degree = len(section) - 1

                if (degree == 1):
                    bezierX = (1 - t_aux) * section[0][0] + t_aux * section[1][0]
                    bezierY = (1 - t_aux) * section[0][1] + t_aux * section[1][1]
                elif (degree == 2):
                    bezierX = pow(1 - t_aux, 2) * section[0][0] + 2 * (1 - t_aux) * t_aux * section[1][0] + pow(t_aux, 2) * section[2][0]
                    bezierY = pow(1 - t_aux, 2) * section[0][1] + 2 * (1 - t_aux) * t_aux * section[1][1] + pow(t_aux, 2) * section[2][1]
                elif (degree == 3):
                    bezierX = pow(1 - t_aux, 3) * section[0][0] + 3 * pow(1 - t_aux, 2) * t_aux * section[1][0] + 3 * (1 - t_aux) * pow(t_aux, 2) * section[2][0] + pow(t_aux, 3) * section[3][0]
                    bezierY = pow(1 - t_aux, 3) * section[0][1] + 3 * pow(1 - t_aux, 2) * t_aux * section[1][1] + 3 * (1 - t_aux) * pow(t_aux, 2) * section[2][1] + pow(t_aux, 3) * section[3][1]
                else:
                    for i in range(degree + 1): 
                        bezierX += BezierSlider.binomial_coef(degree, i) * pow(1 - t_aux, degree - i) * pow(t_aux, i) * section[i][0]
                        bezierY += BezierSlider.binomial_coef(degree, i) * pow(1 - t_aux, degree - i) * pow(t_aux, i) * section[i][1]
            
                t_aux += t
                curr_dist = dist((bezierX, bezierY), point)
                total_distance += curr_dist
                dist_to_last += curr_dist
                point = (bezierX, bezierY)    

                if dist_to_last >= min_dist:
                    dist_to_last -= min_dist
                    path.append(
                        Point(
                            bezierX,
                            bezierY,
                            offset + (total_distance / length) * duration
                        )
                    )

        return path

    @staticmethod
    def binomial_coef(n, k):
        result = 1

        if k > n:
            return 0
        
        for i in range(1, k + 1):
            result *= n
            n -= 1
            result /= i

        return result

    @staticmethod
    def load_coefficient():
        BezierSlider.coefficient = max(0.001, min(get_bezier_coefficient(), 0.1))

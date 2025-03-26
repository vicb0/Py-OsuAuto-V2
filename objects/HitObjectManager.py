from math import dist

from objects.Metadata import Metadata
from objects.HitObject import HitObject
from objects.TimingPointManager import TimingPointManager


class HitObjectManager:
    hos = []
    idx = 0

    @staticmethod
    def add(hit_object: HitObject):
        HitObjectManager.hos.append(hit_object)

    @staticmethod
    def reset():
        HitObjectManager.hos.clear()
        HitObjectManager.idx = 0

    @staticmethod
    def next_ho():
        HitObjectManager.idx += 1

    @staticmethod
    def get(offset=0):
        return HitObjectManager.hos[HitObjectManager.idx + offset]
    
    @staticmethod
    def is_inbound(offset=0):
        return HitObjectManager.idx + offset < len(HitObjectManager.hos)

    @staticmethod
    def fix_stacks():
        # Thanks to https://github.com/idMysteries/osuAutoBot/blob/fe45335697bc5200163be162c39ba595868b7c1b/main.cpp#L446
        # Honestly, this is overly complicated.
        # I thought my own version of stacks was working perfectly until I found a single edge case,
        # Then I found another... and another... and...
        # Finding this code was a blessing

        for i in range(len(HitObjectManager.hos) - 1, 0, -1):
            n = i

            ho_i = HitObjectManager.hos[i]

            if ho_i.stack_id != 0 or ho_i.object_type == 3:
                continue

            if ho_i.object_type == 1:
                n -= 1
                while n >= 0:
                    ho_n = HitObjectManager.hos[n]

                    if ho_n.object_type == 3:
                        n -= 1
                        continue

                    time_i = ho_i.point.offset - Metadata.stack_time
                    time_n = ho_n.point.offset
                    if ho_n.object_type == 2:
                        time_n += ho_n.duration

                    if time_i > time_n:
                        break

                    ho_n_end_pos = ho_n.point if ho_n.object_type == 1 else ho_n.path[-1]
                    if ho_n.object_type != 1 and dist(ho_n_end_pos.get_point(), ho_i.point.get_point()) < 3:
                        offset = ho_i.stack_id - ho_n.stack_id + 1
                        for j in range(n + 1, i + 1):
                            if dist(ho_n_end_pos.get_point(), HitObjectManager.hos[j].point.get_point()) < 3:
                                HitObjectManager.hos[j].stack_id -= offset
                        break
                
                    if dist(ho_n.point.get_point(), ho_i.point.get_point()) < 3:
                        ho_n.stack_id = ho_i.stack_id + 1
                        ho_i = ho_n

                    n -= 1
            elif ho_i.object_type == 2:
                n -= 1
                while n >= 0:
                    ho_n = HitObjectManager.hos[n]

                    if ho_n.object_type == 3:
                        n -= 1
                        continue

                    if ho_i.point.offset - Metadata.stack_time > ho_n.point.offset:
                        break
                    
                    ho_n_end_pos = ho_n.point if ho_n.object_type == 1 else ho_n.path[-1]
                    if dist(ho_n_end_pos.get_point() if ho_n.object_type != 1 else ho_n.point.get_point(), ho_i.point.get_point()) < 3:
                        ho_n.stack_id = ho_i.stack_id + 1
                        ho_i = ho_n
                    n -= 1

        for ho in HitObjectManager.hos:
            ho.stack()

    @staticmethod
    def calc_slider_paths():
        for ho in HitObjectManager.hos:
            while TimingPointManager.is_inbound(+1) and ho.point.offset >= TimingPointManager.get(1).offset:
                TimingPointManager.next_tp()

            if ho.object_type == 2:
                ho.calc_duration()
                ho.get_sections()
                ho.calc_path()
                ho.calc_repeats()

    def calc_spinners():
        for ho in HitObjectManager.hos:
            if ho.object_type == 3:
                ho.calc_path()

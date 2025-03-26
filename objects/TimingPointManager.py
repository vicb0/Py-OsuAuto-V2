from objects.TimingPoint import TimingPoint


class TimingPointManager:
    idx = 0
    tps = []

    @staticmethod
    def add(timing_point: TimingPoint):
        TimingPointManager.tps.append(timing_point)

    @staticmethod
    def reset():
        TimingPointManager.tps.clear()
        TimingPointManager.idx = 0

    @staticmethod
    def next_tp():
        TimingPointManager.idx += 1
    
    @staticmethod
    def get(offset=0):
        return TimingPointManager.tps[TimingPointManager.idx + offset]

    @staticmethod
    def is_inbound(offset=0):
        return TimingPointManager.idx + offset < len(TimingPointManager.tps)

class Metadata:
    stack_leniency = None
    circle_size = None
    approach_rate = None
    slider_multiplier = None

    double_time = False
    hard_rock = False
    easy = False
    half_time = False
    speed_const = 1

    approach_window = None
    stack_offset = None
    stack_time = None

    @staticmethod
    def set_SL(val):
        Metadata.stack_leniency = float(val)

    @staticmethod
    def set_CS(val):
        Metadata.circle_size = float(val)

        if Metadata.easy:
            Metadata.circle_size /= 2
        elif Metadata.hard_rock:
            Metadata.circle_size *= 1.3

    @staticmethod
    def set_AR(val):
        Metadata.approach_rate = float(val)

        if Metadata.easy:
            Metadata.approach_rate /= 2
        elif Metadata.hard_rock:
            Metadata.approach_rate = min(10, Metadata.approach_rate * 1.4)

    @staticmethod
    def set_SM(val):
        Metadata.slider_multiplier = float(val)

    @staticmethod
    def toggle_DT():
        if Metadata.double_time:
            Metadata.speed_const = 1
            Metadata.double_time = False
        else:
            Metadata.speed_const = 2 / 3
            Metadata.double_time = True
            Metadata.half_time = False

    @staticmethod
    def toggle_HT():
        if Metadata.half_time:
            Metadata.speed_const = 1
            Metadata.half_time = False
        else:
            Metadata.speed_const = 4 / 3
            Metadata.half_time = True
            Metadata.double_time = False

    @staticmethod
    def toggle_HR():
        if Metadata.hard_rock:
            Metadata.hard_rock = False
        else:
            Metadata.hard_rock = True
            Metadata.easy = False

    @staticmethod
    def toggle_EZ():
        if Metadata.easy:
            Metadata.easy = False
        else:
            Metadata.easy = True
            Metadata.hard_rock = False
    
    @staticmethod
    def calc_approach_window(min_=1800, mid_=1200, max_=450):
        AR = Metadata.approach_rate

        if AR > 5:
            Metadata.approach_window = mid_ + (max_ - mid_) * (AR - 5) / 5
        elif AR < 5:
            Metadata.approach_window = mid_ - (mid_ - min_) * (5 - AR) / 5
        else:
            Metadata.approach_window = mid_
    
    @staticmethod
    def calc_stack_time():
        Metadata.stack_time = Metadata.approach_window * Metadata.stack_leniency * Metadata.speed_const

    @staticmethod
    def calc_stack_offset():
        Metadata.stack_offset = (512 / 16) * (1 - 0.7 * (Metadata.circle_size - 5.0) / 5.0) / 10.0

    @staticmethod
    def calc_data():
        Metadata.calc_approach_window()
        Metadata.calc_stack_time()
        Metadata.calc_stack_offset()

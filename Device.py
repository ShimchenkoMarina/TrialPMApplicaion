class DeviceState:
    def __init__(self, state_num, state_color, state_text):
        self.num = state_num
        self.color = state_color
        self.text = state_text


class Device:
    def __init__(self, name):
        self.name = name
        self.states = []
        self.colors = {}
        self.order = 0
        self.flag_change = 0

    def add_state(self, tick, state):
        if not isinstance(state, DeviceState):
            raise TypeError("Argument must be type of DeviceState")
        self.states.insert(tick, state)
        length = len(self.states)
        if (self.states[length - 1 ].num != self.states[length - 2].num):
            self.flag_change = self.flag_change + 1

    def set_state_color(self, state, color):
        self.colors[state] = color

    def __repr__(self):
        return repr((self.name, self.order))


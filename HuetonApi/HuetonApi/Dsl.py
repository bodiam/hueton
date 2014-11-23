class bridge:
    class light:
        def __init__(self, id):
            self.id = id

        def turn_on(self):
            print("turned on light {}".format(self.id))
            return self

        def turn_off(self):
            print("turned off light {}".format(self.id))
            return self

        def blink(self, duration=1000):
            print("blinking light {} for {} ms".format(self.id, duration))
            return self

        def colorize(self, start=None, end=None, duration=None):
            print("colorizing light {} from {} to {} in {} ms".format(self.id, start, end, duration))
            return self


bridge.light(1).turn_on().colorize(start='red', end='green', duration=20).colorize(start='green', end='yello', duration=40).turn_off()
import Utils


class basicAutonomous:

    def __init__(self):
        self.target = None
        self.position_epsilon = 3

    def set_target(self, target):
        self.target = target

    def go(self, location, heading):
        assert self.target is not None
        desiredHeading = Utils.bearing(location, self.target)
        if desiredHeading > 0:
            return min(desiredHeading, 100)
        return max(desiredHeading, -100)

    def is_done(self, location):
        if Utils.unscaledDist(self.target, location) <= self.position_epsilon:
            return True
        return False


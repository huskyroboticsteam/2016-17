import Utils


class basicAutonomous:

    def __init__(self):
        self.target = None
        self.position_epsilon = 3

    def set_target(self, target):
        self.target = target

    def go(self, location, heading):
        assert self.target is not None
        desired_heading = Utils.bearing(location, self.target)
        diff_heading = desired_heading - heading
        while diff_heading > 180.0:
            diff_heading -= 360.0
        while diff_heading < -180.0:
            diff_heading += 360.0
        if diff_heading > 0:
            return min(diff_heading, 100)
        return max(diff_heading, -100)

    def is_done(self, location):
        if Utils.unscaledDist(self.target, location) <= self.position_epsilon:
            return True
        return False


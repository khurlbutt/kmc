

class Site(object):

    def __init__(self, coordinates, state):
        assert coordinates
        assert isinstance(state, str) and state  # "*_0", "A", "CO", "O2", etc.

        # eg (x, y, s) or (r, theta, s) or something else, up to YOU!
        self.coordinates = tuple(coordinates)
        self.state = state
        # TODO gets updated now, but should we show in __repr__?
        self.last_update_step = 0

    def transition(self, step, state):
        self.last_update_step = step
        self.state = state

    def __repr__(self):
        return "@%r%s" % (self.coordinates, self.state)

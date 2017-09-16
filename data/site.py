

class Site(object):

    def __init__(self, coordinates, state):
        assert coordinates
        assert isinstance(state, str) and state  # "*_0", "A", "CO", "O2", etc.

        # eg (x, y, s) or (r, theta, s) or something else, up to YOU!
        self.coordinates = tuple(coordinates)
        self.state = state
        # TODO
        self.last_update_step = 0

    def __repr__(self):
        return "@%r%s" % (self.coordinates, self.state)

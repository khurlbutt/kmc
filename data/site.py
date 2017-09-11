

class Site(object):

    def __init__(self, coordinates, state):
        self.coordinates = tuple(coordinates)
        self.state = state
        # TODO
        self.last_update_step = None

    def __repr__(self):
        return "@%r%s" % (self.coordinates, self.state)

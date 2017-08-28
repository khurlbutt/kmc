

class Cell(object):

    def __init__(self, row, col, num_sites=None, sites=None):

        # User-defined indices map to a particular model.
        # TODO: Okay to assume empty sites are occupied by a hole of some kind?
        def _initialize_sites(num_sites, sites=None):
            if not num_sites and not sites:
                raise CellException("Uninitialized sites")
            if sites:
                return sites
            return ["*_%d" % index for index in range(num_sites)]

        self.row = row
        self.col = col
        # TODO: Okay to assume empty sites are occupied by a hole of some kind?
        self.sites = _initialize_sites(num_sites or 0, sites=sites)

    def __repr__(self):
        return "(%d,%d)%r" % (self.row, self.col, self.sites)


class CellException(Exception):
    pass

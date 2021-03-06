import data.lattice


class Cell(object):

    def __init__(self, lattice, coordinates):
        assert isinstance(lattice, data.lattice.Lattice)
        assert isinstance(lattice.coordinate_cardinalities, tuple)
        assert lattice.coordinate_cardinalities
        num_sites = lattice.coordinate_cardinalities[-1]
        assert isinstance(num_sites, int) and num_sites > 0
        assert coordinates
        assert len(coordinates) == len(lattice.coordinate_cardinalities) - 1

        self.coordinates = tuple(coordinates)  # eg (x, y)
        sites_coordinates = [self.coordinates + (index, )
            for index in range(num_sites)]
        self._sites = {site_coordinates: lattice[site_coordinates]
            for site_coordinates in sites_coordinates}

    def site_states(self):
        for site in self:
            yield site.state

    def __iter__(self):
        for site_coordinates in sorted(self._sites):
            yield self._sites[site_coordinates]

    def __repr__(self):
        return "%r,%r" % (self.coordinates, list(self.site_states()))


class CellException(Exception):
    pass

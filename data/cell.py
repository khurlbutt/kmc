import data.site


class Cell(object):

    def __init__(self, coordinates, num_sites):
        assert isinstance(num_sites, int) and num_sites > 0

        self.coordinates = tuple(coordinates)  # eg (x, y)
        # eg (x, y, s) or (r, theta, s) or something else, up to YOU!
        # TODO: Okay to assume empty sites are occupied by a hole of some kind?
        sites_coordinates = [self.coordinates + (index, )
            for index in range(num_sites)]
        empty_sites = [data.site.Site(site_coordinates, "*_%d" % index)
            for index, site_coordinates in enumerate(sites_coordinates)]
        self.sites = {site_coordinates: empty_site
            for site_coordinates, empty_site in zip(
                sites_coordinates, empty_sites)}

    def site_states(self):
        for site in self:
            yield site.state

    def __iter__(self):
        for site_coordinates in sorted(self.sites):
            yield self.sites[site_coordinates]

    def __repr__(self):
        return "%r,%r" % (self.coordinates, list(self.site_states()))


class CellException(Exception):
    pass

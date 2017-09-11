import itertools
import data.cell


class Lattice(object):

    def __init__(self, *, axis_lengths=None, num_sites=None):
        self.coordinante_cardinalites = axis_lengths or (2, 2)

        axis_sets = [list(range(cc)) for cc in self.coordinante_cardinalites]
        # Default to (x, y) here. But (r, theta, z) is equally chill.
        coordinate_points = list(itertools.product(*axis_sets))
        empty_cells = [data.cell.Cell(cell_coordinates, num_sites or 1)
            for cell_coordinates in coordinate_points]
        self.cells = {cell.coordinates: cell for cell in empty_cells}

        # Ends up storing all the site bookkeeping twice... here and on cells.
        self.sites = {}
        for cell in self.iter_cells():
            for site in cell:
                self.sites[site.coordinates] = site

    def iter_cells(self):
        # Example of a generator-iterator as described by PEP 255.
        # Intro to generators as "lazy evaluation" or "calculation on demand":
        #   http://intermediatepythonista.com/python-generators
        for cell_coordinates in sorted(self.cells):
            yield self.cells[cell_coordinates]

    def iter_sites(self):
        for cell in self.iter_cells():
            for site in cell:
                yield site

    def __repr__(self):
        species_counts = {}
        for site in self.iter_sites():
            species_counts[site.state] = species_counts.get(site.state, 0) + 1
        # TODO: Okay to assume empty sites are occupied by a hole of some kind?
        total_count = sum([count for species, count in species_counts.items()])
        dist = {}
        for species, count in species_counts.items():
            dist[species] = count / total_count
        sorted_distribution = [(s, "%.2f" % p) for s, p in sorted(
            dist.items(), key=lambda item: item[1], reverse=True)]
        return "(%r){%r unique species: %r}" % (
            "x".join([str(c) for c in self.coordinante_cardinalites]),
            len(species_counts), sorted_distribution)

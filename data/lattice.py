import data.cell


class Lattice(object):

    def __init__(self, length=None, width=None, num_sites=None):
        self.length = length or 2
        self.width = width or 2
        self.cells = [[data.cell.Cell(row, col, num_sites=num_sites or 1)
            for col in range(self.width)] for row in range(self.length)]

    def enumerate_cells(self):
        # Example of a generator-iterator as described by PEP 255.
        # Intro to generators as "lazy evaluation" or "calculation on demand":
        #   http://intermediatepythonista.com/python-generators
        for row in range(self.length):
            for col in range(self.width):
                yield self.cells[row][col]

    def __repr__(self):
        species_counts = {}
        for cell in self.enumerate_cells():
            for site in cell.sites:
                species_counts[site] = species_counts.get(site, 0) + 1
        dist = {}
        # TODO: Okay to assume empty sites are occupied by a hole of some kind?
        total_count = sum([count
            for species, count in species_counts.items()])
        for species, count in species_counts.items():
            dist[species] = count / total_count
        sorted_distribution = [(s, "%.2f" % p) for s, p in sorted(
            dist.items(), key=lambda item: item[1], reverse=True)]
        return "(%dx%d){%r unique species: %r}" % (self.length, self.width,
            len(species_counts), sorted_distribution)

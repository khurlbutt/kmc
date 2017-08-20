
class Lattice(object):

    def __init__(self, length=None, width=None, num_sites=None):
        self.length = length or 2
        self.width = width or 2
        self.cells = [[Cell(row, col, num_sites=num_sites or 1)
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
            for adsorbate in cell.get_adsorbates():
                species_counts[adsorbate] = species_counts.get(adsorbate, 0) + 1
        dist = {}
        # Does not assume holes, but include holes if present.
        total_count = sum([adsorbate_count
            for species, adsorbate_count in species_counts.items()])
        for species, adsorbate_count in species_counts.items():
            dist[species] = adsorbate_count / total_count
        sorted_distribution = [(s, "%.2f" % p) for s, p in sorted(
            dist.items(), key=lambda item: item[1], reverse=True)]
        return "(%d,%d){%r unique species: %r}" % (self.length, self.width,
            len(species_counts), sorted_distribution)


class Cell(object):

    def __init__(self, row, col, num_sites=None, sites=None):

        # User-defined indices map to a particular model.
        # TODO: Okay to assume empty sites are occupied by a hole of some kind?
        def _initialize_sites(num_sites, sites=None):
            if not num_sites and not sites:
                raise CellException("Uninitialized sites")
            if sites and len(sites) == num_sites:
                return sites
            return ["*_%d" % index for index in range(num_sites)]

        self.row = row
        self.col = col
        self.sites = _initialize_sites(num_sites or 0, sites=sites)

    # TODO: Okay to assume empty sites are occupied by a hole of some kind?
    def get_adsorbates(self):
        return [adsorbate if adsorbate else "*_%d" % index
            for index, adsorbate in enumerate(self.sites)]

    def __repr__(self):
        return "(%d,%d)%r" % (self.row, self.col, self.sites)


class Process(object):

    def __init__(self, est_perform_time, cell, is_enabled_still_fn, perform_fn):
        # From what I can tell a simple model might use 4 inputs:
        # est_perform_time : estimated time(step) of occurence
        # cell : lattice cell in question
        # is_enabled_still_fn : method to know if process still "allowed" after
        #                       considering lattice changes since entry into
        #                       EnabledCollection, i.e. a "null event" check
        # perform_fn : method for performing what process would do if enacted
        self.est_perform_time = est_perform_time
        # TODO: Only cell indices
        self.cell = cell
        # TODO: Only 2-tuple, e.g. index of function template, cell indices
        # TODO: This must invalidate processes involving sites updated since
        #       process est_perform_time to avoid oversampling expired processes
        #       that otherwise meet enablement criteria.
        self._is_enabled_still_fn = is_enabled_still_fn
        # TODO: Only 2-tuple, e.g. index of function template, cell indices
        self._perform_fn = perform_fn
        self._is_performed = False

    def perform(self):
        if not self.is_still_performable():
            raise LatticeProcessException("Not performable")
        self._perform_fn(self.cell)
        self._is_performed = True

    def is_still_performable(self):
        # Assumes that references to cell sites updated elsewhere. Eventually,
        # may need to reference neighbors using cell.row or cell.col.
        return not self._is_performed and self._is_enabled_still_fn(self.cell)

    def is_performed(self):
        return bool(self._is_performed)

    def __repr__(self):
        return "%r" % [
            self.est_perform_time,
            (self.cell.row, self.cell.col),
            ("is_performed", self.is_performed()),
            ("_is_enabled_still_fn", self._is_enabled_still_fn),
            ("_perform_fn", self._perform_fn)]


class EnabledCollection(object):

    def __init__(self):
        # Requirements:
        # Add element, log n
        # Pop lowest value (for est_perform_time), log n
        #
        # Nice to have:
        #
        # Current top ideas:
        # Red-black tree
        #
        pass


class CellException(Exception):
    pass


class LatticeProcessException(Exception):
    pass


def main():
    import print_toys
    print_toys.lattice_examples()
    print_toys.process_examples()


if __name__ == '__main__':
    main()

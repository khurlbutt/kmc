
class Simulation(object):

    def __init__(self):
        self.lattice = Lattice()
        self.process_queue = EnabledCollection(key_fn=Process.time_value)
        self.time = 0  # Let's try staying integer/usec, can discuss options.
        # Enable processes
        # Draw a process, perform if possible, add new enabled processes.
        # (Repeat above)

    def __repr__(self):
        return "t=%d\nLattice:%r\nEnabledCollection:%r" % (
            self.time, self.lattice, self.process_queue)


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


class Process(object):

    def __init__(self, est_perform_time, cell, is_enabled_still_fn, perform_fn):
        # From what I can tell a simple model might use 4 inputs:
        # est_perform_time : estimated time(step) of occurence
        # cell : lattice cell in question
        # is_enabled_still_fn : method to know if process still "allowed" after
        #                       considering lattice changes since entry into
        #                       EnabledCollection, i.e. a "null event" check
        # perform_fn : method for performing what process would do if enacted
        self._est_perform_time = est_perform_time
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

    def time_value(self):
        return int(self._est_perform_time)

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
            self._est_perform_time,
            (self.cell.row, self.cell.col),
            ("is_performed", self.is_performed()),
            ("_is_enabled_still_fn", self._is_enabled_still_fn),
            ("_perform_fn", self._perform_fn)]


class EnabledCollection(object):

    def __init__(self, key_fn=None):
        # Requirements:
        # Add element, log n
        # Pop lowest value (for est_perform_time), log n
        #
        # Nice to have:
        # Evict expired processes eg prune values < x, min(# pruned, log n)
        #
        # Current top ideas:
        # SortedListWithKey
        # http://www.grantjenks.com/docs/sortedcontainers/sortedlistwithkey.html
        # IMHO this will do for early iterating; we could build our own, but
        # honestly this is likely more performant. As a plus, it's pythonic AF.
        assert key_fn, "Need callable for sorted process queue."
        import sortedcontainers
        self._queue = sortedcontainers.SortedListWithKey(key=key_fn)

    def add(self, process):
        # Assumes estimated performace time used as key.
        self._queue.add(process)

    def pop(self, raise_if_empty=False):
        try:
            return self._queue.pop(0)
        except IndexError as e:
            if raise_if_empty:
                raise e
            return None

    def __repr__(self):
        return "%d process%s, queue:%r" % (
            len(self._queue),
            "es" if len(self._queue) != 1 else "",
            self._queue
        )


class CellException(Exception):
    pass


class LatticeProcessException(Exception):
    pass


def main():
    import print_toys
    print_toys.lattice_examples()
    print_toys.process_examples()
    print_toys.enabled_collection_examples()

    print_toys.simulation_examples()


if __name__ == '__main__':
    main()

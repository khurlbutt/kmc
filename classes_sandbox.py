
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

    def __init__(self, sim_time, cell, is_enabled_still_fn, perform_fn):
        # From what I can tell a simple model might use 4 inputs:
        # sim_time : estimated time(step) of occurence
        # cell : lattice cell in question
        # is_enabled_still_fn : method to know if process still "allowed" after
        #                       considering lattice changes since entry into
        #                       EnabledCollection, i.e. a "null event" check
        # perform_fn : method for performing what process would do if enacted
        self.sim_time = sim_time
        # TODO: Only cell indices
        self.cell = cell
        # TODO: Only 2-tuple, e.g. index of function template, cell indices
        # TODO: This must invalidate processes involving sites updated since
        #       process sim_time to avoid oversampling expired processes that
        #       otherwise meet enablement criteria.
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
            self.sim_time,
            (self.cell.row, self.cell.col),
            ("is_performed", self.is_performed()),
            ("_is_enabled_still_fn", self._is_enabled_still_fn),
            ("_perform_fn", self._perform_fn)]


class EnabledCollection(object):

    def __init__(self):
        # Requirements:
        # Add element, log n
        # Pop lowest value (for sim_time), log n
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


def print_toy_lattice_examples():
    for num_sites in range(1, 5):
        print("\n\n%d site(s) per cell:" %
            num_sites)
        lattice = Lattice(length=2, width=2, num_sites=num_sites)
        if num_sites == 1:
            lattice.cells[0][0].sites = ["A"]
        elif num_sites == 2:
            lattice.cells[0][0].sites = ["O2", "CO"]
            lattice.cells[0][1].sites = ["*_0", "CO"]
            lattice.cells[1][0].sites = ["O2", "*_1"]
        elif num_sites == 3:
            lattice.cells[0][0].sites = ["X_bridge", "Y_bridge", "*_2"]
            lattice.cells[0][1].sites = ["*_0", "*_1", "Z_hollow"]
            lattice.cells[1][0].sites = ["X_bridge", "*_1", "Z_hollow"]
            lattice.cells[1][1].sites = ["*_0", "Y_bridge", "Z_hollow"]
        else:
            # Exists a dist of "allowed" occupants, dependpent on cell's state.
            example_sites = ["<draw_allowable(cell, site_%d)>" % index
                for index in range(num_sites)]
            lattice.cells[0][0].sites = example_sites

        print("Lattice: %r" % lattice)
        for cell in lattice.enumerate_cells():
            print(cell)


def print_toy_process_examples():
    for num_sites in range(1, 6):
        lattice = Lattice(length=2, width=2, num_sites=num_sites)
        process = None
        if num_sites == 1:
            def _still_allowed_fn(cell):
                return cell.get_adsorbates() == ["A"]

            def _perform_fn(cell):
                cell.sites = ["*_0"]
            cell = lattice.cells[0][0]
            cell.sites = ["A"]
            sim_time = 10  # Whatever
            remove = Process(sim_time, cell, _still_allowed_fn, _perform_fn)
            process = remove
            print("\n\nREMOVAL: %d site(s) per cell" % num_sites)
        if num_sites == 5:
            def _still_allowed_fn(cell):
                # We could check individual site or use patterns etc.
                # return bool(
                #     cell.sites[0] == "*_0" and
                #     cell.sites[1] == "*_1" and
                #     cell.sites[2] == "CO2" and
                #     cell.sites[3] == "CO2" and
                #     cell.sites[4] == "*_4")
                return cell.sites == ["*_0", "*_1", "CO2", "CO2", "*_4"]

            def _perform_fn(cell):
                cell.sites = ["CO", "CO", "*_2", "*_4", "O2"]
            cell = lattice.cells[0][0]
            cell.sites = ["*_0", "*_1", "CO2", "CO2", "*_4"]
            sim_time = 10  # Whatever
            breakdown = Process(sim_time, cell, _still_allowed_fn, _perform_fn)
            process = breakdown
            print("\n\nBREAKDOWN: %d site(s) per cell" % num_sites)
        if process:
            print("before")
            print("Lattice:%r" % lattice)
            print("Process:%r" % process)
            print(process.cell)
            process.perform()
            print("after")
            print("Lattice:%r" % lattice)
            print("Process:%r" % process)
            print(process.cell)


def main():
    print_toy_lattice_examples()
    print_toy_process_examples()


if __name__ == '__main__':
    main()
